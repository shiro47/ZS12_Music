// NAVBAR
document.addEventListener("DOMContentLoaded", function(event) {
   
    const showNavbar = (toggleId, navId, bodyId, headerId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)
    
    // Validate that all variables exist
    if(toggle && nav && bodypd && headerpd){
    toggle.addEventListener('click', ()=>{
    // show navbar
    nav.classList.toggle('show')
    // change icon
    toggle.classList.toggle('bx-x')
    // add padding to body
    bodypd.classList.toggle('body-pd')
    // add padding to header
    headerpd.classList.toggle('body-pd')
    })
    }
    }
    
    showNavbar('header-toggle','nav-bar','body-pd','header')
    
    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link')
    
    function colorLink(){
    if(linkColor){
    linkColor.forEach(l=> l.classList.remove('active'))
    this.classList.add('active')
    }
    }
    linkColor.forEach(l=> l.addEventListener('click', colorLink))
    
     // Your code to run since DOM is loaded and ready
    });


// AJAXS

function submit_bug() {
    $.ajax({
        type: $('#report_bug_form').attr('method'),
        url: $('#report_bug_form').attr('action'),
        data: $('#report_bug_form').serialize(),
        beforeSend: function(){
            // Show image container
            document.getElementById("loader").style.display = "block";
           },
        success: function (resp) {
            var x = document.getElementById("snackbar");
            x.innerHTML = resp.message;
            x.className = "show";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
        },   
        complete: function(){
            // Hide image container
            document.getElementById("loader").style.display = "none";
        },
    });
}

function submit_delete(id) {
    $.ajax({
        type: $('#delete_form_'+id).attr('method'),
        url: $('#delete_form_'+id).attr('action'),
        data: $('#delete_form_'+id).serialize(),
        beforeSend: function(){
            // Show image container
            document.getElementById("loader").style.display = "block";
           },
        success: function (data) {
            $("#song_"+id).fadeOut("slow");
        },
        complete: function(){
            // Hide image container
            document.getElementById("loader").style.display = "none";
        },   
    });
}

function clear_queue() {
    $.ajax({
        type: "POST",
        url: "{% url 'songrequestapp:clear_queue' %}",
        data: { csrfmiddlewaretoken: "{{ csrf_token }}",
        state:"inactive" 
        },
        beforeSend: function(){
            // Show image container
            document.getElementById("loader").style.display = "block";
        },
        success: function (data) {
            $("#songs_queue").fadeOut("slow");
            $("#song_player").fadeOut("slow");
            $("#control_panel").fadeOut("slow");
            document.getElementById("songs_status").style.visibility = "visible";
        },
        complete: function(){
            // Hide image container
            document.getElementById("loader").style.display = "none";
        },    
    });
}

function submit_song_to_blacklist(id) {
    $.ajax({
        type: $('#submit_form_to_blacklist'+id).attr('method'),
        url: $('#submit_form_to_blacklist'+id).attr('action'),
        data: $('#submit_form_to_blacklist'+id).serialize(),
        beforeSend: function(){
            // Show image container
            document.getElementById("loader").style.display = "block";
        },
        success: function (data) {
            $("#song_"+id).fadeOut("slow");
        },
        complete: function(){
            // Hide image container
            document.getElementById("loader").style.display = "none";
        },    
    });
}

function submit_song_from_history(id) {
    $.ajax({
        type: $('#request-song-'+id).attr('method'),
        url: $('#request-song-'+id).attr('action'),
        data: $('#request-song-'+id).serialize(),
        beforeSend: function(){
            // Show image container
            document.getElementById("loader").style.display = "block";
           },
        success: function (resp) {
            var x = document.getElementById("snackbar");
            x.innerHTML = resp.message;
            x.className = "show";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
        },
        complete: function(){
            // Hide image container
            document.getElementById("loader").style.display = "none";
        },
    });
}

function submit_delete_from_history(id) {
    $.ajax({
        type: $('#delete_form_'+id).attr('method'),
        url: $('#delete_form_'+id).attr('action'),
        data: $('#delete_form_'+id).serialize(),
        beforeSend: function(){
            // Show image container
            document.getElementById("loader").style.display = "block";
           },
        success: function (resp) {
            $("#song_"+id).fadeOut("slow");
        },
        complete: function(){
            // Hide image container
            document.getElementById("loader").style.display = "none";
        },   
    });
}

function submit_song() {
    $.ajax({
        type: $('#request-song').attr('method'),
        url: $('#request-song').attr('action'),
        data: $('#request-song').serialize(),
        beforeSend: function(){
            // Show image container
            document.getElementById("loader").style.display = "block";
           },
        success: function (resp) {
            var x = document.getElementById("snackbar");
            x.innerHTML = resp.message;
            x.className = "show";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
        },   
        complete: function(){
            // Hide image container
            document.getElementById("loader").style.display = "none";
        },
    });
}

function submit_skip_vote(id) {
    $.ajax({
        type: $('#skip_vote_'+id).attr('method'),
        url: $('#skip_vote_'+id).attr('action'),
        data: $('#skip_vote_'+id).serialize(),
        beforeSend: function(){
            // Show image container
            document.getElementById("loader").style.display = "block";
           },
        success: function (resp) {
            var x = document.getElementById("snackbar");
            x.innerHTML = resp.message;
            x.className = "show";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
            
        },   
        complete: function(){
            // Hide image container
            document.getElementById("loader").style.display = "none";
        },
    });
}

function submit_delete_from_blacklist(id) {
    $.ajax({
        type: $('#delete_from_blacklist'+id).attr('method'),
        url: $('#delete_from_blacklist'+id).attr('action'),
        data: $('#delete_from_blacklist'+id).serialize(),
        beforeSend: function(){
            // Show image container
            document.getElementById("loader").style.display = "block";
           },
        success: function (resp) {
            var x = document.getElementById("snackbar");
            x.innerHTML = resp.message;
            x.className = "show";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
            $("#song_"+id).fadeOut("slow");
        },
        complete: function(){
            // Hide image container
            document.getElementById("loader").style.display = "none";
        },   
    });
}