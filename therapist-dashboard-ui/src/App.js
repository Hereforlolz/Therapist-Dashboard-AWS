import React, { useState, useEffect } from 'react';

const API_BASE = process.env.REACT_APP_API_BASE_URL;

export default function App() {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [sessionNotes, setSessionNotes] = useState('');
  const [patientContext, setPatientContext] = useState('');
  const [insight, setInsight] = useState(null);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Fetch patients
  useEffect(() => {
    fetch(`${API_BASE}/dashboard`)
      .then((res) => res.json())
      .then((data) => setPatients(data.patients || []))
      .catch(console.error);
  }, []);

  // Select patient handler
  const selectPatient = (patient) => {
    setSelectedPatient(patient);
    setSummary(patient.summary || '');
    setInsight(null);
    setSessionNotes('');
    setPatientContext('');
    setMessage('');
  };

  // Generate Insight API call
  const generateInsight = async () => {
    if (!sessionNotes.trim()) {
      setMessage('Session notes are required for insight generation.');
      return;
    }
    setLoading(true);
    setMessage('');
    try {
      const res = await fetch(`${API_BASE}/insight`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_notes: sessionNotes,
          patient_context: patientContext,
        }),
      });
      const data = await res.json();
      if (res.ok) setInsight(data.insight);
      else setMessage(data.message || 'Error generating insight');
    } catch (e) {
      setMessage('Error calling insight API');
    } finally {
      setLoading(false);
    }
  };

  // Save Summary API call
  const saveSummary = async () => {
    if (!selectedPatient) return;
    if (!summary.trim()) {
      setMessage('Summary cannot be empty.');
      return;
    }
    setLoading(true);
    setMessage('');
    try {
      const res = await fetch(`${API_BASE}/summary`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: selectedPatient.patient_id,
          summary,
          session_notes: sessionNotes,
        }),
      });
      const data = await res.json();
      if (res.ok) {
        setMessage('Summary saved successfully.');
        // Update local patient summary
        setPatients((ps) =>
          ps.map((p) =>
            p.patient_id === selectedPatient.patient_id ? { ...p, summary } : p
          )
        );
      } else {
        setMessage(data.message || 'Error saving summary');
      }
    } catch (e) {
      setMessage('Error calling summary API');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: 'auto', fontFamily: 'Arial, sans-serif', padding: 20 }}>
      <h1>Therapist Dashboard AI</h1>

      <section style={{ marginBottom: 20 }}>
        <h2>Patients</h2>
        {patients.length === 0 && <p>No patients found.</p>}
        <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
          {patients.map((p) => (
            <li
              key={p.patient_id}
              onClick={() => selectPatient(p)}
              style={{
                cursor: 'pointer',
                padding: '6px 10px',
                backgroundColor:
                  selectedPatient?.patient_id === p.patient_id ? '#d0f0fd' : '#f0f0f0',
                marginBottom: 6,
                borderRadius: 4,
              }}
            >
              {p.name} ({p.status})
            </li>
          ))}
        </ul>
      </section>

      {selectedPatient && (
        <section>
          <h2>Patient: {selectedPatient.name}</h2>
          <p>
            <strong>Last Visit:</strong> {selectedPatient.last_visit}
          </p>
          <p>
            <strong>Current Summary:</strong> {selectedPatient.summary || '(No summary)'}
          </p>

          <textarea
            rows={4}
            style={{ width: '100%', marginBottom: 10 }}
            placeholder="Session notes for insight generation..."
            value={sessionNotes}
            onChange={(e) => setSessionNotes(e.target.value)}
          />

          <textarea
            rows={2}
            style={{ width: '100%', marginBottom: 10 }}
            placeholder="Optional: Patient context (age, diagnosis, etc.)"
            value={patientContext}
            onChange={(e) => setPatientContext(e.target.value)}
          />

          <button onClick={generateInsight} disabled={loading} style={{ marginRight: 10 }}>
            {loading ? 'Generating...' : 'Generate Insight'}
          </button>

          {insight && (
            <pre
              style={{
                whiteSpace: 'pre-wrap',
                backgroundColor: '#eef6ff',
                padding: 10,
                marginTop: 10,
                borderRadius: 4,
                maxHeight: 200,
                overflowY: 'auto',
              }}
            >
              {insight}
            </pre>
          )}

          <h3>Edit Summary</h3>
          <textarea
            rows={4}
            style={{ width: '100%', marginBottom: 10 }}
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
          />

          <button onClick={saveSummary} disabled={loading}>
            {loading ? 'Saving...' : 'Save Summary'}
          </button>

          {message && (
            <p style={{ marginTop: 10, color: message.toLowerCase().includes('error') ? 'red' : 'green' }}>
              {message}
            </p>
          )}
        </section>
      )}
    </div>
  );
}
