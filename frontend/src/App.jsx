import { useState, useEffect } from 'react'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard') // dashboard | structure | import
  const [subStructureTab, setSubStructureTab] = useState('dept') // dept | filiere | parcours

  // --- DONNÉES DE STRUCTURE SÉCURISÉES DEPUIS LA BDD ---
  const [structure, setStructure] = useState({ diplomes: [], departements: [], filieres: [], parcours: [] })

  // --- FORMULAIRES DE SAISIE / MODIFICATION ---
  const [formDept, setFormDept] = useState({ id: null, intitule_fr: '', intitule_ar: '' })
  const [formFiliere, setFormFiliere] = useState({ id: null, code: '', intitule_fr: '', intitule_ar: '', departement_id: '', diplome_id: '' })
  const [formParcours, setFormParcours] = useState({ id: null, code: '', intitule_fr: '', intitule_ar: '', filiere_id: '', diplome_id: '' })

  // --- ÉTATS DASHBOARD ET IMPORTATION ---
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [crudMessage, setCrudMessage] = useState('')

  // Charger la structure académique globale au démarrage
  const loadStructure = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/structure/')
      const data = await response.json()
      setStructure(data)
    } catch (e) { console.error("Erreur de chargement de la structure", e) }
  }

  useEffect(() => {
    loadStructure()
  }, [])

  // --- ACTIONS SOUCHAMP CRUD ---
  const handleSaveDept = async (e) => {
    e.preventDefault()
    const res = await fetch('http://127.0.0.1:8000/manage-departement/', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formDept)
    })
    const data = await res.json()
    setCrudMessage(res.ok ? `✅ ${data.message}` : `❌ ${data.detail}`)
    setFormDept({ id: null, intitule_fr: '', intitule_ar: '' })
    loadStructure()
  }

  const handleSaveFiliere = async (e) => {
    e.preventDefault()
    const res = await fetch('http://127.0.0.1:8000/manage-filiere/', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formFiliere)
    })
    const data = await res.json()
    setCrudMessage(res.ok ? `✅ ${data.message}` : `❌ ${data.detail}`)
    if (res.ok) setFormFiliere({ id: null, code: '', intitule_fr: '', intitule_ar: '', departement_id: '', diplome_id: '' })
    loadStructure()
  }

  const handleSaveParcours = async (e) => {
    e.preventDefault()
    const res = await fetch('http://127.0.0.1:8000/manage-parcours/', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formParcours)
    })
    const data = await res.json()
    setCrudMessage(res.ok ? `✅ ${data.message}` : `❌ ${data.detail}`)
    if (res.ok) setFormParcours({ id: null, code: '', intitule_fr: '', intitule_ar: '', filiere_id: '', diplome_id: '' })
    loadStructure()
  }

  return (
    <div style={{ maxWidth: '1000px', margin: '30px auto', fontFamily: 'system-ui, sans-serif', padding: '0 20px' }}>
      
      {/* BARRE DE NAVIGATION PRINCIPALE */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid #e2e8f0', paddingBottom: '15px', marginBottom: '25px' }}>
        <h2 style={{ margin: 0, color: '#0f172a' }}>🎓 USMBA Scolarité LMD</h2>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={() => setActiveTab('dashboard')} style={{ padding: '8px 16px', borderRadius: '6px', fontWeight: 'bold', border: 'none', cursor: 'pointer', backgroundColor: activeTab === 'dashboard' ? '#0f172a' : '#e2e8f0', color: activeTab === 'dashboard' ? 'white' : '#475569' }}>🔍 Recherche</button>
          <button onClick={() => setActiveTab('structure')} style={{ padding: '8px 16px', borderRadius: '6px', fontWeight: 'bold', border: 'none', cursor: 'pointer', backgroundColor: activeTab === 'structure' ? '#0f172a' : '#e2e8f0', color: activeTab === 'structure' ? 'white' : '#475569' }}>🗂️ Structure & Saisie</button>
          <button onClick={() => setActiveTab('import')} style={{ padding: '8px 16px', borderRadius: '6px', fontWeight: 'bold', border: 'none', cursor: 'pointer', backgroundColor: activeTab === 'import' ? '#0f172a' : '#e2e8f0', color: activeTab === 'import' ? 'white' : '#475569' }}>📥 Imports Excel</button>
        </div>
      </div>

      {crudMessage && <div onClick={() => setCrudMessage('')} style={{ padding: '12px', borderRadius: '6px', marginBottom: '20px', backgroundColor: '#f0fdf4', color: '#166534', border: '1px solid #bbf7d0', fontWeight: '500', cursor: 'pointer' }}>{crudMessage}</div>}

      {/* ================= COMPOSANT STRUCTURE & SAISIE MANUELLE ================= */}
      {activeTab === 'structure' && (
        <div>
          {/* Sous-Menu Structure */}
          <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', backgroundColor: '#f1f5f9', padding: '6px', borderRadius: '8px' }}>
            <button onClick={() => setSubStructureTab('dept')} style={{ flex: 1, padding: '8px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', backgroundColor: subStructureTab === 'dept' ? '#fff' : 'transparent', boxShadow: subStructureTab === 'dept' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none' }}>1. Départements</button>
            <button onClick={() => setSubStructureTab('filiere')} style={{ flex: 1, padding: '8px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', backgroundColor: subStructureTab === 'filiere' ? '#fff' : 'transparent', boxShadow: subStructureTab === 'filiere' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none' }}>2. Filières Principales</button>
            <button onClick={() => setSubStructureTab('parcours')} style={{ flex: 1, padding: '8px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', backgroundColor: subStructureTab === 'parcours' ? '#fff' : 'transparent', boxShadow: subStructureTab === 'parcours' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none' }}>3. Parcours / Options</button>
          </div>

          {/* SECTION DÉPARTEMENTS */}
          {subStructureTab === 'dept' && (
            <div style={{ display: 'flex', gap: '25px' }}>
              <form onSubmit={handleSaveDept} style={{ width: '350px', backgroundColor: '#f8fafc', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0', height: 'fit-content' }}>
                <h4>{formDept.id ? "✏️ Modifier le Département" : "➕ Nouveau Département"}</h4>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Intitulé Français</label>
                <input type="text" value={formDept.intitule_fr} onChange={e => setFormDept({...formDept, intitule_fr: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }} required />
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Intitulé Arabe</label>
                <input type="text" value={formDept.intitule_ar} onChange={e => setFormDept({...formDept, intitule_ar: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1', textAlign: 'right' }} required />
                <button type="submit" style={{ width: '100%', marginTop: '15px', padding: '10px', backgroundColor: '#0284c7', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}>Enregistrer</button>
                {formDept.id && <button type="button" onClick={() => setFormDept({id:null, intitule_fr:'', intitule_ar:''})} style={{ width: '100%', marginTop: '5px', padding: '6px', backgroundColor: '#64748b', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Annuler</button>}
              </form>
              <div style={{ flex: 1 }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
                  <thead><tr style={{ backgroundColor: '#f1f5f9', textAlign: 'left' }}><th style={{ padding: '10px' }}>ID</th><th style={{ padding: '10px' }}>Département (FR)</th><th style={{ padding: '10px', textAlign: 'right' }}>Département (AR)</th><th style={{ padding: '10px' }}>Actions</th></tr></thead>
                  <tbody>{structure.departements.map(d => (<tr key={d.id} style={{ borderBottom: '1px solid #e2e8f0' }}><td style={{ padding: '10px' }}>{d.id}</td><td style={{ padding: '10px', fontWeight: '600' }}>{d.intitule_fr}</td><td style={{ padding: '10px', textAlign: 'right' }}>{d.intitule_ar}</td><td style={{ padding: '10px' }}><button onClick={() => setFormDept(d)} style={{ padding: '4px 8px', backgroundColor: '#e2e8f0', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Modifier</button></td></tr>))}</tbody>
                </table>
              </div>
            </div>
          )}

          {/* SECTION FILIÈRES */}
          {subStructureTab === 'filiere' && (
            <div style={{ display: 'flex', gap: '25px' }}>
              <form onSubmit={handleSaveFiliere} style={{ width: '350px', backgroundColor: '#f8fafc', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0', height: 'fit-content' }}>
                <h4>{formFiliere.id ? "✏️ Modifier la Filière" : "➕ Nouvelle Filière"}</h4>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Code Filière (ex: SEG)</label>
                <input type="text" value={formFiliere.code} onChange={e => setFormFiliere({...formFiliere, code: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }} required />
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Nom Filière (FR)</label>
                <input type="text" value={formFiliere.intitule_fr} onChange={e => setFormFiliere({...formFiliere, intitule_fr: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }} required />
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Nom Filière (AR)</label>
                <input type="text" value={formFiliere.intitule_ar} onChange={e => setFormFiliere({...formFiliere, intitule_ar: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1', textAlign: 'right' }} required />
                
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Département Parent</label>
                <select value={formFiliere.departement_id} onChange={e => setFormFiliere({...formFiliere, departement_id: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px' }} required>
                  <option value="">-- Choisir --</option>
                  {structure.departements.map(d => <option key={d.id} value={d.id}>{d.intitule_fr}</option>)}
                </select>

                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Diplôme Associé</label>
                <select value={formFiliere.diplome_id} onChange={e => setFormFiliere({...formFiliere, diplome_id: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px' }} required>
                  <option value="">-- Choisir --</option>
                  {structure.diplomes.map(d => <option key={d.id} value={d.id}>{d.intitule_fr}</option>)}
                </select>

                <button type="submit" style={{ width: '100%', marginTop: '15px', padding: '10px', backgroundColor: '#0284c7', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}>Enregistrer</button>
                {formFiliere.id && <button type="button" onClick={() => setFormFiliere({id:null, code:'', intitule_fr:'', intitule_ar:'', departement_id:'', diplome_id:''})} style={{ width: '100%', marginTop: '5px', padding: '6px', backgroundColor: '#64748b', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Annuler</button>}
              </form>
              <div style={{ flex: 1, overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
                  <thead><tr style={{ backgroundColor: '#f1f5f9', textAlign: 'left' }}><th style={{ padding: '8px' }}>Code</th><th style={{ padding: '8px' }}>Filière (FR)</th><th style={{ padding: '8px' }}>Département</th><th style={{ padding: '8px' }}>Actions</th></tr></thead>
                  <tbody>{structure.filieres.map(f => {
                    const dept = structure.departements.find(d => d.id === f.departement_id);
                    return (<tr key={f.id} style={{ borderBottom: '1px solid #e2e8f0' }}><td style={{ padding: '8px', fontWeight: 'bold', color: '#0284c7' }}>{f.code}</td><td style={{ padding: '8px' }}>{f.intitule_fr}</td><td style={{ padding: '8px', color: '#64748b' }}>{dept ? dept.intitule_fr : 'Inconnu'}</td><td style={{ padding: '8px' }}><button onClick={() => setFormFiliere(f)} style={{ padding: '3px 6px', backgroundColor: '#e2e8f0', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Modifier</button></td></tr>)
                  })}</tbody>
                </table>
              </div>
            </div>
          )}

          {/* SECTION PARCOURS */}
          {subStructureTab === 'parcours' && (
            <div style={{ display: 'flex', gap: '25px' }}>
              <form onSubmit={handleSaveParcours} style={{ width: '350px', backgroundColor: '#f8fafc', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0', height: 'fit-content' }}>
                <h4>{formParcours.id ? "✏️ Modifier le Parcours" : "➕ Nouveau Parcours"}</h4>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Code Parcours (ex: GES)</label>
                <input type="text" value={formParcours.code} onChange={e => setFormParcours({...formParcours, code: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }} required />
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Nom Option (FR)</label>
                <input type="text" value={formParcours.intitule_fr} onChange={e => setFormParcours({...formParcours, intitule_fr: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }} required />
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Nom Option (AR)</label>
                <input type="text" value={formParcours.intitule_ar} onChange={e => setFormParcours({...formParcours, intitule_ar: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1', textAlign: 'right' }} required />
                
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Filière Tronc Commun Parente</label>
                <select value={formParcours.filiere_id} onChange={e => setFormParcours({...formParcours, filiere_id: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px' }} required>
                  <option value="">-- Choisir --</option>
                  {structure.filieres.map(f => <option key={f.id} value={f.id}>{f.code} - {f.intitule_fr}</option>)}
                </select>

                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', margin: '10px 0 5px 0' }}>Diplôme Associé</label>
                <select value={formParcours.diplome_id} onChange={e => setFormParcours({...formParcours, diplome_id: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px' }} required>
                  <option value="">-- Choisir --</option>
                  {structure.diplomes.map(d => <option key={d.id} value={d.id}>{d.intitule_fr}</option>)}
                </select>

                <button type="submit" style={{ width: '100%', marginTop: '15px', padding: '10px', backgroundColor: '#0284c7', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}>Enregistrer</button>
                {formParcours.id && <button type="button" onClick={() => setFormParcours({id:null, code:'', intitule_fr:'', intitule_ar:'', filiere_id:'', diplome_id:''})} style={{ width: '100%', marginTop: '5px', padding: '6px', backgroundColor: '#64748b', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Annuler</button>}
              </form>
              <div style={{ flex: 1, overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
                  <thead><tr style={{ backgroundColor: '#f1f5f9', textAlign: 'left' }}><th style={{ padding: '8px' }}>Code</th><th style={{ padding: '8px' }}>Parcours (FR)</th><th style={{ padding: '8px' }}>Filière Parent</th><th style={{ padding: '8px' }}>Actions</th></tr></thead>
                  <tbody>{structure.parcours.map(p => {
                    const fil = structure.filieres.find(f => f.id === p.filiere_id);
                    return (<tr key={p.id} style={{ borderBottom: '1px solid #e2e8f0' }}><td style={{ padding: '8px', fontWeight: 'bold', color: '#10b981' }}>{p.code}</td><td style={{ padding: '8px' }}>{p.intitule_fr}</td><td style={{ padding: '8px', color: '#64748b' }}>{fil ? fil.code : 'Inconnu'}</td><td style={{ padding: '8px' }}><button onClick={() => setFormParcours(p)} style={{ padding: '3px 6px', backgroundColor: '#e2e8f0', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Modifier</button></td></tr>)
                  })}</tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ================= ANCIENS ONGLETS (DASHBOARD & IMPORTS) ================= */}
      {/* ... [Laissez ici vos blocs existants de Recherche et d'Importation créés précédemment] ... */}
    </div>
  )
}

export default App