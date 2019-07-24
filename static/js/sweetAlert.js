function mes_e() {
	Swal.fire({
	  type: 'error',
	  title: 'Oops...',
	  text: 'Something went wrong!',
	  footer: '<a href>Link</a>'
	})
}


function mes_s() {
	Swal.fire({
	  type: 'success',
	  title: 'Good...',
	  text: 'Something went wrong!'
	})
}

 
function messagge(){
	const Toast = Swal.mixin({
	  toast: true,
	  position: 'top-end',
	  showConfirmButton: false,
	  timer: 4000
	});

	Toast.fire({
	  type: 'success',
	  title: 'parame'
	})
}