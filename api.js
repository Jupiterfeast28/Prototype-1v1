// Simple frontend helpers to call backend API endpoints

async function postJob(payload) {
  try {
    const res = await fetch('/api/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return await res.json();
  } catch (err) {
    console.error('postJob error', err);
    throw err;
  }
}

async function postResume(payload) {
  try {
    const res = await fetch('/api/resumes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return await res.json();
  } catch (err) {
    console.error('postResume error', err);
    throw err;
  }
}

function showMessage(el, text, isError) {
  if (!el) return alert(text);
  el.textContent = text;
  el.style.color = isError ? 'crimson' : 'green';
  setTimeout(() => { el.textContent = ''; }, 5000);
}

document.addEventListener('DOMContentLoaded', () => {
  // Bind post a job form
  const jobForm = document.getElementById('jobForm');
  const jobMsg = document.createElement('div');
  jobMsg.id = 'jobMessage';
  jobMsg.style.marginTop = '12px';
  if (jobForm) jobForm.appendChild(jobMsg);

  jobForm && jobForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      title: document.getElementById('jobTitle')?.value || '',
      description: document.getElementById('jobDescription')?.value || '',
      location: document.getElementById('location')?.value || '',
      // Optional fields
      employer_id: null,
    };
    try {
      const created = await postJob(payload);
      showMessage(jobMsg, 'Job created (ID: ' + (created.job_id || created.jobId || created.id || '?') + ')');
      jobForm.reset();
    } catch (err) {
      showMessage(jobMsg, 'Failed to create job', true);
    }
  });

  // Landing page resume upload (metadata-only stub)
  const uploadBtn = document.getElementById('uploadBtn');
  const resumeInput = document.getElementById('resumeInput');
  const uploadMsg = document.createElement('div');
  uploadMsg.id = 'uploadMessage';
  uploadMsg.style.marginTop = '8px';
  if (uploadBtn && uploadBtn.parentNode) uploadBtn.parentNode.appendChild(uploadMsg);

  uploadBtn && uploadBtn.addEventListener('click', (ev) => {
    ev.preventDefault();
    resumeInput && resumeInput.click();
  });

  resumeInput && resumeInput.addEventListener('change', async (ev) => {
    const file = ev.target.files && ev.target.files[0];
    if (!file) return;
    const payload = {
      candidate_id: null,
      file_name: file.name,
      file_type: file.type || 'application/octet-stream'
    };
    try {
      const created = await postResume(payload);
      showMessage(uploadMsg, 'Resume metadata saved (id: ' + (created.resume_id || created.id || '?') + ')');
      resumeInput.value = '';
    } catch (err) {
      showMessage(uploadMsg, 'Upload failed', true);
    }
  });
});
