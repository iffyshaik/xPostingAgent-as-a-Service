// frontend/src/pages/SubmitTopic.tsx
import React, { useState } from 'react';
import Input from '../components/Input';
import Select from '../components/Select';
import Layout from '../components/Layout';
import { submitTopic } from '../api';
import api from "../api";


const SubmitTopic: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [contentType, setContentType] = useState('thread');
  const [platform, setPlatform] = useState('typefully');
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Advanced settings
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [persona, setPersona] = useState("Professional and engaging");
  const [tone, setTone] = useState('');
  const [style, setStyle] = useState('');
  const [language, setLanguage] = useState('');
  const [autoPost, setAutoPost] = useState(false);
  const [includeCitations, setIncludeCitations] = useState(false);


  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setLoading(true);
  setSuccessMsg('');
  setErrorMsg('');

  try {
    // Step 1: Prepare the request payload
    const payload: any = {
      original_topic: topic,
      content_type: contentType,
      platform,
      auto_post: autoPost,
      include_source_citations: includeCitations,
    };

    // ✅ Add persona if filled in
    if (persona) {
      payload.persona = persona;
    }

    // Step 2: Submit the topic
    const res = await submitTopic(payload);
    const requestId = res.request_id;

    // Step 3: Run the full agent pipeline
    await api.post(`/pipeline/${requestId}/topic`);
    await api.post(`/pipeline/${requestId}/research`);
    await api.post(`/pipeline/${requestId}/summary`);
    await api.post(`/pipeline/${requestId}/content`);

    // Step 4: Show final result
    if (autoPost) {
      setSuccessMsg('✅ Content was posted successfully!');
    } else {
      setSuccessMsg('📝 Content generated. You can review it on the dashboard.');
    }

    // Clear form
    setTopic('');
  } catch (error: any) {
    console.error(error);
    setErrorMsg(error?.response?.data?.error || 'Submission failed.');
  } finally {
    setLoading(false);
  }
};


  // const handleSubmit = async (e: React.FormEvent) => {
  //   e.preventDefault();
  //   setLoading(true);
  //   setSuccessMsg('');
  //   setErrorMsg('');

  //   try {
  //     const payload: any = {
  //       original_topic: topic,
  //       content_type: contentType,
  //       platform,
  //       auto_post: autoPost,
  //       include_source_citations: includeCitations,
  //     };

  //     //if (tone) payload.tone = tone;
  //     //if (style) payload.style = style;
  //     //if (language) payload.language = language;

  //     await submitTopic(payload);
  //     setSuccessMsg('Topic submitted successfully!');
  //     setTopic('');
  //   } catch (error: any) {
  //     setErrorMsg(error?.response?.data?.error || 'Submission failed.');
  //   } finally {
  //     setLoading(false);
  //   }
  // };



  return (
    <>
      <div className="max-w-xl mx-auto mt-10">
        <h1 className="text-2xl font-semibold mb-6">Submit New Topic</h1>
        <form onSubmit={handleSubmit}>
          <Input
            label="Topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. AI in fertility medicine"
          />
          <Select
            label="Content Type"
            value={contentType}
            onChange={(e) => setContentType(e.target.value)}
            options={[
              { value: 'thread', label: 'Thread' },
              { value: 'article', label: 'Article' },
            ]}
          />
          <Select
            label="Platform"
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            options={[
              { value: 'typefully', label: 'Typefully' },
              { value: 'x', label: 'X (Twitter)' },
            ]}
          />

          <div className="mb-4">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={autoPost}
                onChange={() => setAutoPost(!autoPost)}
              />
              <span>Auto-post after generation</span>
            </label>
          </div>

          <div className="mb-4">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={includeCitations}
                onChange={() => setIncludeCitations(!includeCitations)}
              />
              <span>Include source citations</span>
            </label>
          </div>

          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-sm text-blue-600 underline mb-4"
          >
            {showAdvanced ? 'Hide' : 'Show'} advanced settings
          </button>

          {showAdvanced && (
            <div className="mb-6 border p-4 rounded-lg bg-gray-50">
              
              {/* ✅ Persona textarea */}
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1" htmlFor="persona">
                  Persona (optional):
                </label>
                <textarea
                  id="persona"
                  value={persona}
                  onChange={(e) => setPersona(e.target.value)}
                  className="w-full border rounded p-2 text-sm"
                  rows={2}
                  placeholder="e.g. Thoughtful, witty, professional tone..."
                />
              </div>
              
              
              
              <Select
                label="Tone"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                options={[
                  { value: '', label: 'Use default' },
                  { value: 'informative', label: 'Informative' },
                  { value: 'funny', label: 'Funny' },
                  { value: 'sarcastic', label: 'Sarcastic' },
                  { value: 'serious', label: 'Serious' },
                ]}
              />

              <Select
                label="Style"
                value={style}
                onChange={(e) => setStyle(e.target.value)}
                options={[
                  { value: '', label: 'Use default' },
                  { value: 'conversational', label: 'Conversational' },
                  { value: 'formal', label: 'Formal' },
                  { value: 'storytelling', label: 'Storytelling' },
                ]}
              />

              <Select
                label="Language"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                options={[
                  { value: '', label: 'Use default' },
                  { value: 'en', label: 'English' },
                  { value: 'es', label: 'Spanish' },
                  { value: 'fr', label: 'French' },
                ]}
              />
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Submitting...' : 'Submit'}
          </button>
        </form>

        {successMsg && <p className="text-green-600 mt-4">{successMsg}</p>}
        {errorMsg && <p className="text-red-600 mt-4">{errorMsg}</p>}
      </div>
    </>
  );
};

export default SubmitTopic;
