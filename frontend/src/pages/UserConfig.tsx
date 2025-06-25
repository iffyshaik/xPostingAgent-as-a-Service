// frontend/src/pages/UserConfig.tsx
import React, { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import Input from '../components/Input';
import Select from '../components/Select';
import api from '../api';

const UserConfig: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [persona, setPersona] = useState('');
  const [tone, setTone] = useState('');
  const [style, setStyle] = useState('');
  const [language, setLanguage] = useState('en');
  const [platformPreference, setPlatformPreference] = useState('typefully');
  const [researchPreference, setResearchPreference] = useState('balanced');

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const res = await api.get('/users/configurations');
        const config = res.data.data;
        setPersona(config.persona || '');
        setTone(config.tone || '');
        setStyle(config.style || '');
        setLanguage(config.language || 'en');
        setPlatformPreference(config.platform_preference || 'typefully');
        setResearchPreference(config.research_preference || 'balanced');
      } catch (err) {
        setError('Failed to load configuration.');
      } finally {
        setLoading(false);
      }
    };

    fetchConfig();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSuccess('');
    setError('');

    try {
      await api.put('/users/configurations', {
        persona,
        tone,
        style,
        language,
        platform_preference: platformPreference,
        research_preference: researchPreference,
      });
      setSuccess('Configuration saved.');
    } catch (err) {
      setError('Failed to save configuration.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Layout><p>Loading...</p></Layout>;

  return (
    <Layout>
      <div className="max-w-xl mx-auto mt-10">
        <h1 className="text-2xl font-semibold mb-6">User Configuration</h1>
        <form onSubmit={handleSave}>
          <Input label="Persona" value={persona} onChange={(e) => setPersona(e.target.value)} />
          <Input label="Tone" value={tone} onChange={(e) => setTone(e.target.value)} />
          <Input label="Style" value={style} onChange={(e) => setStyle(e.target.value)} />

          <Select
            label="Language"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            options={[
              { value: 'en', label: 'English' },
              { value: 'es', label: 'Spanish' },
              { value: 'fr', label: 'French' },
              { value: 'de', label: 'German' },
            ]}
          />
          <Select
            label="Research Preference"
            value={researchPreference}
            onChange={(e) => setResearchPreference(e.target.value)}
            options={[
              { value: 'general', label: 'General' },
              { value: 'science_heavy', label: 'Science Heavy' },
              { value: 'balanced', label: 'Balanced' },
            ]}
          />
          <Select
            label="Default Platform"
            value={platformPreference}
            onChange={(e) => setPlatformPreference(e.target.value)}
            options={[
              { value: 'typefully', label: 'Typefully' },
              { value: 'x', label: 'X (Twitter)' },
            ]}
          />

          <button
            type="submit"
            disabled={saving}
            className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 mt-4"
          >
            {saving ? 'Saving...' : 'Save Configuration'}
          </button>
        </form>

        {success && <p className="text-green-600 mt-4">{success}</p>}
        {error && <p className="text-red-600 mt-4">{error}</p>}
      </div>
    </Layout>
  );
};

export default UserConfig;
