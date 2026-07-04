import { useState } from 'react'

function App() {
  const [diplomaType, setDiplomaType] = useState('DEUG')
  const [anneeUniversitaire, setAnneeUniversitaire] = useState('2025/2026')
  const [studentFiles, setStudentFiles] = useState([])
  const [marksFilesData, setMarksFilesData] = useState([])
  
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [unmatchedStudents, setUnmatchedStudents] = useState([]) // NOUVEAU : Liste des anomalies

  const diplomaOptions = ["DEUG", "Licence", "Licence Fondamentale", "Master"]

  const handleMarksFilesSelect = (e) => {
    const files = Array.from(e.target.files)
    setMarksFilesData(files.map(f => ({ file: f, date: '' })))
  }

  const handleDateChange = (index, newDate) => {
    const updated = [...marksFilesData]
    updated[index].date = newDate
    setMarksFilesData(updated)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setMessage('')
    setUnmatchedStudents([]) // Réinitialiser les alertes

    const missingDate = marksFilesData.some(item => !item.date)
    if (studentFiles.length === 0 || marksFilesData.length === 0 || missingDate) {
      setMessage("❌ Veuillez configurer tous les fichiers et leurs dates de délibération.")
      setIsLoading(false)
      return
    }

    const formData = new FormData()
    formData.append('diploma_type', diplomaType)
    formData.append('annee_universitaire', anneeUniversitaire)

    for (let i = 0; i < studentFiles.length; i++) {
      formData.append('students_files', studentFiles[i])
    }

    marksFilesData.forEach(item => {
      formData.append('marks_files', item.file)
      formData.append('deliberation_dates', item.date)
    })

    try {
      const response = await fetch('http://127.0.0.1:8000/upload-data/', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      
      if (response.ok) {
        setMessage(`✅ ${data.message}`)
        // Si le serveur a détecté des étudiants manquants, on les enregistre dans le state
        if (data.unmatched_students && data.unmatched_students.length > 0) {
          setUnmatchedStudents(data.unmatched_students)
        }
      } else {
        setMessage(`❌ Erreur: ${data.detail}`)
      }
    } catch (error) {
      setMessage(`❌ Erreur: ${error.message}`)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '650px', margin: '50px auto', fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ border: '1px solid #ddd', padding: '30px', borderRadius: '10px', backgroundColor: '#fff', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '20px', color: '#1e293b' }}>Chargement des Données Académiques</h2>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '5px' }}>Type de Diplôme</label>
            <select value={diplomaType} onChange={(e) => setDiplomaType(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}>
              {diplomaOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
            </select>
          </div>

          <div>
            <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '5px' }}>Année Universitaire</label>
            <input type="text" value={anneeUniversitaire} onChange={(e) => setAnneeUniversitaire(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
          </div>

          <hr style={{ margin: '10px 0', border: 'none', borderTop: '1px solid #e2e8f0' }} />

          <div>
            <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '5px' }}>1. Fichiers Données Personnelles (Excel)</label>
            <input type="file" accept=".xlsx, .xls" multiple onChange={(e) => setStudentFiles(e.target.files)} style={{ width: '100%' }} />
          </div>

          <div style={{ backgroundColor: '#f8fafc', padding: '15px', borderRadius: '5px', border: '1px solid #e2e8f0' }}>
            <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '10px', color: '#334155' }}>2. Fichiers de Notes et Délibérations</label>
            <input type="file" accept=".xlsx, .xls" multiple onChange={handleMarksFilesSelect} style={{ width: '100%', marginBottom: '10px' }} />
            
            {marksFilesData.map((item, index) => (
              <div key={index} style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '10px', fontSize: '14px' }}>
                <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', color: '#475569' }}>📄 {item.file.name}</span>
                <input 
                  type="date" 
                  value={item.date} 
                  onChange={(e) => handleDateChange(index, e.target.value)} 
                  style={{ padding: '6px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                  required
                />
              </div>
            ))}
          </div>

          <button type="submit" disabled={isLoading} style={{ padding: '12px', backgroundColor: isLoading ? '#94a3b8' : '#2563eb', color: 'white', fontWeight: 'bold', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
            {isLoading ? 'Vérification et Traitement...' : 'Vérifier et Enregistrer les données'}
          </button>
        </form>
        
        {message && (
          <div style={{ marginTop: '20px', padding: '15px', borderRadius: '5px', backgroundColor: message.includes('❌') ? '#fee2e2' : '#d1fae5', color: message.includes('❌') ? '#991b1b' : '#065f46', border: '1px solid' }}>
            {message}
          </div>
        )}

        {/* SECTION ALERTES : Étudiants introuvables */}
        {unmatchedStudents.length > 0 && (
          <div style={{ marginTop: '25px', padding: '20px', borderRadius: '8px', backgroundColor: '#fffbeb', border: '1px solid #fef3c7' }}>
            <h3 style={{ color: '#b45309', margin: '0 0 10px 0', fontSize: '16px' }}>⚠️ Alerte: Étudiants introuvables dans les fiches personnelles</h3>
            <p style={{ color: '#78350f', fontSize: '14px', margin: '0 0 15px 0' }}>
              Les {unmatchedStudents.length} étudiants suivants possèdent des notes mais n'ont pas été enregistrés car leur CNE n'existe pas dans le fichier de données personnelles :
            </p>
            <div style={{ maxHeight: '180px', overflowY: 'auto', border: '1px solid #fde68a', borderRadius: '4px', backgroundColor: '#fff' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
                <thead>
                  <tr style={{ backgroundColor: '#fef3c7', color: '#78350f' }}>
                    <th style={{ padding: '8px', borderBottom: '1px solid #fde68a' }}>CNE / Code Attalib</th>
                    <th style={{ padding: '8px', borderBottom: '1px solid #fde68a' }}>Nom complet (Fichier Notes)</th>
                  </tr>
                </thead>
                <tbody>
                  {unmatchedStudents.map((st, idx) => (
                    <tr key={idx} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '8px', fontWeight: '500', color: '#ef4444' }}>{st.cne}</td>
                      <td style={{ padding: '8px', color: '#334155' }}>{st.nom_complet}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App