import json
import boto3
import logging
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime')

PATIENTS_TABLE = 'patients'
BEDROCK_MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }

def get_dashboard(event, context):
    try:
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 50))
        last_key = query_params.get('last_key')

        table = dynamodb.Table(PATIENTS_TABLE)
        scan_params = {
            'Limit': min(limit, 100),
            'ProjectionExpression': 'patient_id, first_name, last_name, last_visit, summary, #st',
            'ExpressionAttributeNames': {'#st': 'status'}
        }

        if last_key:
            try:
                scan_params['ExclusiveStartKey'] = json.loads(last_key)
            except json.JSONDecodeError:
                logger.warning(f"Invalid last_key format: {last_key}")

        response = table.scan(**scan_params)

        patients = []
        for item in response.get('Items', []):
            patients.append({
                'patient_id': item.get('patient_id'),
                'name': f"{item.get('first_name', '')} {item.get('last_name', '')}".strip(),
                'last_visit': item.get('last_visit'),
                'summary': item.get('summary', ''),
                'status': item.get('status', 'active')
            })

        result = {'patients': patients, 'count': len(patients)}

        if 'LastEvaluatedKey' in response:
            result['next_key'] = json.dumps(response['LastEvaluatedKey'], cls=DecimalEncoder)

        logger.info(f"Retrieved {len(patients)} patients")
        return create_response(200, result)

    except ClientError as e:
        logger.error(f"DynamoDB error: {str(e)}")
        return create_response(500, {'error': 'Database error', 'message': 'Unable to retrieve patient data'})
    except Exception as e:
        logger.error(f"Unexpected error in get_dashboard: {str(e)}")
        return create_response(500, {'error': 'Internal server error', 'message': 'An unexpected error occurred'})

def generate_insight(event, context):
    try:
        if not event.get('body'):
            return create_response(400, {'error': 'Missing request body', 'message': 'Session notes are required'})

        body = json.loads(event['body'])
        session_notes = body.get('session_notes', '').strip()
        patient_context = body.get('patient_context', '')

        if not session_notes:
            return create_response(400, {'error': 'Missing session notes', 'message': 'Session notes cannot be empty'})

        user_message = f"""You are a compassionate healthcare assistant helping to generate gentle insights from therapy session notes. Please provide supportive, professional insights focused on patient progress and well-being.

Session Notes:
{session_notes}

{f"Patient Context: {patient_context}" if patient_context else ""}

Please provide:
1. Key themes or patterns observed
2. Signs of progress or positive developments
3. Areas that may benefit from continued attention
4. Gentle recommendations for future sessions

Keep your response supportive, professional, and focused on the patient's growth and healing journey."""

        bedrock_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }

        response = bedrock.invoke_model(
            modelId=BEDROCK_MODEL_ID,  # should still be: 'anthropic.claude-3-sonnet-20240229-v1:0'
            body=json.dumps(bedrock_body)
        )

        response_text = response['body'].read().decode('utf-8')
        response_body = json.loads(response_text)

        insight = response_body.get("content", "")
        if isinstance(insight, list):  # sometimes the response is a list of message parts
            insight = ''.join(part.get('text', '') for part in insight)

        if not insight:
            logger.warning("Bedrock response missing insight content")
            insight = "No insight generated."

        result = {
            'insight': insight,
            'generated_at': datetime.utcnow().isoformat(),
            'model_used': BEDROCK_MODEL_ID
        }
        logger.info("Generated insight successfully")
        return create_response(200, result)

    except ClientError as e:
        logger.error(f"Bedrock error: {str(e)}")
        return create_response(500, {'error': 'AI service error', 'message': 'Unable to generate insights at this time'})
    except Exception as e:
        logger.error(f"Unexpected error in generate_insight: {str(e)}")
        return create_response(500, {'error': 'Internal server error', 'message': 'An unexpected error occurred'})


def save_summary(event, context):
    try:
        if not event.get('body'):
            return create_response(400, {'error': 'Missing request body', 'message': 'Patient ID and summary are required'})

        body = json.loads(event['body'])
        patient_id = body.get('patient_id', '').strip()
        summary = body.get('summary', '').strip()
        session_notes = body.get('session_notes', '')

        if not patient_id:
            return create_response(400, {'error': 'Missing patient ID', 'message': 'Patient ID is required'})
        if not summary:
            return create_response(400, {'error': 'Missing summary', 'message': 'Summary cannot be empty'})

        table = dynamodb.Table(PATIENTS_TABLE)

        update_expression = 'SET summary = :summary, last_updated = :timestamp'
        expression_values = {
            ':summary': summary,
            ':timestamp': datetime.utcnow().isoformat()
        }
        if session_notes:
            update_expression += ', latest_session_notes = :notes'
            expression_values[':notes'] = session_notes

        response = table.update_item(
            Key={'patient_id': patient_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues='ALL_NEW',
            ConditionExpression='attribute_exists(patient_id)'
        )

        updated = response['Attributes']
        result = {'patient_id': updated['patient_id'], 'summary': updated['summary'], 'last_updated': updated['last_updated'], 'message': 'Summary updated successfully'}

        logger.info(f"Updated summary for patient {patient_id}")
        return create_response(200, result)

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logger.warning(f"Patient not found: {patient_id}")
            return create_response(404, {'error': 'Patient not found', 'message': f'No patient with ID: {patient_id}'})
        logger.error(f"DynamoDB error: {str(e)}")
        return create_response(500, {'error': 'Database error', 'message': 'Unable to save patient summary'})
    except Exception as e:
        logger.error(f"Unexpected error in save_summary: {str(e)}")
        return create_response(500, {'error': 'Internal server error', 'message': 'An unexpected error occurred'})
