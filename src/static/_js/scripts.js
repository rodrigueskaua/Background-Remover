document.addEventListener('DOMContentLoaded', function () {

  const imageForm = document.getElementById('image-form');
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');
  const imagePreview = document.getElementById('image-preview');
  let uploadedFiles = []; 

  dropZone.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
      handleFiles(fileInput.files);
    }
  });

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length) {
      fileInput.files = files; 
      handleFiles(files);
    }
  });

  function handleFiles(files) {
    for (const file of files) {
      if (!file.type.startsWith('image/')) continue;
      
      uploadedFiles.push(file);

      const reader = new FileReader();
      reader.onload = (e) => {
        const previewItem = document.createElement('div');
        previewItem.className = 'preview-item';
        
        const fileIndex = uploadedFiles.length - 1; 
        previewItem.dataset.fileIndex = fileIndex;

        previewItem.innerHTML = `
          <img src="${e.target.result}" alt="${file.name}">
          <button type="button" class="remove-btn" title="Remover">&times;</button>
        `;
        imagePreview.appendChild(previewItem);
      };
      reader.readAsDataURL(file);
    }
  }

  imagePreview.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-btn')) {
      const previewItem = e.target.closest('.preview-item');
      const fileIndexToRemove = parseInt(previewItem.dataset.fileIndex, 10);
      
      uploadedFiles[fileIndexToRemove] = null;
      
      previewItem.remove();
    }
  });


  imageForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData();
    const urlsValue = document.querySelector('textarea[name="urls"]').value;
    const validFiles = uploadedFiles.filter(file => file !== null);
    
    if (validFiles.length === 0 && urlsValue.trim() === '') {
        Swal.fire('Atenção!', 'Por favor, adicione pelo menos uma imagem ou URL.', 'warning');
        return;
    }

    validFiles.forEach(file => { formData.append('files[]', file); });
    formData.append('urls', urlsValue);

    Swal.fire({
      title: 'Aguarde...',
      text: 'Estamos processando suas imagens.',
      icon: 'info',
      allowOutsideClick: false,
      showConfirmButton: false,
      didOpen: () => { Swal.showLoading(); }
    });

    fetch(imageForm.action, {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (!response.ok) {
          return response.json().then(err => { throw new Error(err.message || 'Ocorreu um erro no servidor.') });
      }
      const header = response.headers.get('Content-Disposition');
      let filename = 'download'; // Nome padrão
      if (header) {
          const parts = header.split(';');
          const filenamePart = parts.find(part => part.trim().startsWith('filename='));
          if (filenamePart) {
              filename = filenamePart.split('=')[1].replaceAll('"', '').trim();
          }
      }
      return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
      Swal.close();
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      
      window.URL.revokeObjectURL(url);
      a.remove();
      
      imagePreview.innerHTML = '';
      uploadedFiles = [];
      imageForm.reset();
    })
    .catch(error => {
      Swal.close();
      Swal.fire('Erro!', error.message, 'error');
      console.error('Error:', error);
    });
  });
});