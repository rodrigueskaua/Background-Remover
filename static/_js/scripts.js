function showAlert(type, message) {
  Swal.fire({
    title: type.charAt(0).toUpperCase() + type.slice(1) + '!',
    text: message,
    icon: type,
    confirmButtonText: 'OK'
  });
}

document.getElementById('convert-button').addEventListener('click', function () {
  let uploadForm = document.getElementById('upload-form');
  let formData = new FormData(uploadForm);

  Swal.fire({
    title: 'Aguarde...',
    text: 'Estamos processando suas imagens.',
    icon: 'info',
    allowOutsideClick: false,
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  fetch(uploadForm.action, {
    method: 'POST',
    body: formData
  }).then(response => response.json()).then(data => {
    Swal.close();
    if (data.success) {
      showAlert('success', data.message);
    } else {
      showAlert('error', data.message);
    }
  }).catch(error => {
    Swal.close();
    showAlert('error', 'Erro ao enviar imagens.');
  });
});