window.onscroll = () => btnTapToTop();

function btnTapToTop() {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    $('#tap_to_top').removeClass('d-none').addClass('d-block')
  } else {
    $('#tap_to_top').removeClass('d-block').addClass('d-none')
  }
}

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

function fillParentId(parentId, parent_username) {
  $("#id_parent").val(parentId);
  // $("#parent_place").val(parentId)
  // .attr('disabled', true);
  $("#id_is_read_by_admin").val(false).attr('disabled', true);
  $('#is_read_by_admin').addClass('d-none');
  $('#response_to').text('در پاسخ به کاربر: ' + parent_username).removeClass('d-none');
  document.getElementById('contactus_form').scrollIntoView({behavior: "smooth"});
  // $('#parent_place').removeClass('d-none');
}

function addFoodToOrder(food_id) {
  const foodCount = $('#food-count-' + food_id).val();

  $.get('/order/add-food-to-order?food_id=' + food_id + '&count=' + foodCount).then(res => {
    $('#my-toast').html(res);
    const toastTrigger = document.getElementById('addFoodButton');
    const toastLive = document.getElementById('FoodToast');
    if (toastTrigger) {
      const toast = new bootstrap.Toast(toastLive)
      toast.show()
    }
  })

  // const toastTrigger = document.getElementById('liveToastBtn')
  // const toastLiveExample = document.getElementById('liveToast')

  // if (toastTrigger) {
  //   const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
  //   toastTrigger.addEventListener('click', () => {
  //     toastBootstrap.show()
  //   })
  // }
}

function removeFoodFromOrder(food_id) {
  $.get('/order/remove-from-order?food_id=' + food_id).then(res => {
    $('#my-toast').html(res);
    const toastTrigger = document.getElementById('removeFoodButton');
    const toastLive = document.getElementById('FoodToast');
    if (toastTrigger) {
      const toast = new bootstrap.Toast(toastLive)
      toast.show()
    }
  })
}

function showModalImage(nameImage, imageSrc) {
  $('#modalImageLabel').text(nameImage)
  $('#modal_image').attr({'src': imageSrc, 'width': 500, 'height': 500})
}


function successCostumePayment(order_id, total_price) {
  $.get('/order/success-payment?order_id=' + order_id + '&total_parice=' + total_price).then(res => {
    if (res.status === 'success') {
      let div_success = `<div class="alert alert-success">${res.message}</div>`;
      $('#buttons').html(div_success)
    } else if ((res.status === 'invalid_food_id') || (res.status === 'not_food_found')) {
      let div_success = `<div class="alert alert-warning">${res.message}</div>`;
      $('#buttons').html(div_success)
    }
  })
}

// else if (res.status === 'not_food_found') {
//       let div_success = `<div class="alert alert-warning">${res.message}</div>`;
//       $('#buttons').html(div_success)
//     } else if (res.status === 'price_zero') {
//       let div_success = `<div class="alert alert-warning">${res.message}</div>`;
//       $('#buttons').html(div_success)
//     }

function cancelCostumePayment(order_id) {
  $.get('/order/cancel-payment?order_id=' + order_id).then(res => {
    if (res.status === 'failed') {
      let div_success = `<div class="alert alert-success">${res.message}</div>`;
      $('#buttons').html(div_success)
    } else if ((res.status === 'invalid_food_id') || (res.status === 'not_food_found')) {
      let div_success = `<div class="alert alert-warning">${res.message}</div>`;
      $('#buttons').html(div_success)
    }
  })
}


// const myModal = document.getElementById('myModal')
// const myInput = document.getElementById('myInput')
//
// myModal.addEventListener('shown.bs.modal', () => {
//   myInput.focus()
// })

// function addRoomToastButton() {
//     const toastTrigger = document.getElementById('addRoomButton')
//     const toast = document.getElementById('addRoomToast')
//     if (toastTrigger) {
//         toastTrigger.addEventListener('click', () => {
//             const toast = new bootstrap.Toast(toast)
//             toast.show()
//         })
//     }
// }

