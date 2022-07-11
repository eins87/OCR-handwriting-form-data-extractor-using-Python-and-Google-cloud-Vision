// set the dropzone container id
const id = "#kt_dropzonejs_example_3";
const dropzone = document.querySelector(id);
const url = "/upload";

// set the preview element template
var previewNode = dropzone.querySelector(".dropzone-item");
previewNode.id = "";
var previewTemplate = previewNode.parentNode.innerHTML;
previewNode.parentNode.removeChild(previewNode);

var myDropzone = new Dropzone(id, { // Make the whole body a dropzone
    url: url, // Set the url for your upload script location
    parallelUploads: 1,
    maxFilesize: 2, // Max filesize in MB
    maxFiles: 1,
    uploadMultiple: false,
    previewTemplate: previewTemplate,
    previewsContainer: id + " .dropzone-items", // Define the container to display the previews
    clickable: id  // Define the element that should be used as click trigger to select files.
});

myDropzone.on("addedfile", function (file) {
    // Hookup the start button
    const dropzoneItems = dropzone.querySelectorAll('.dropzone-item');
    dropzoneItems.forEach(dropzoneItem => {
        dropzoneItem.style.display = '';
    });
});

// Update the total progress bar
myDropzone.on("totaluploadprogress", function (progress) {
    const progressBars = dropzone.querySelectorAll('.progress-bar');
    progressBars.forEach(progressBar => {
        progressBar.style.width = progress + "%";
    });
});

myDropzone.on("sending", function (file) {
    // Show the total progress bar when upload starts
    const progressBars = dropzone.querySelectorAll('.progress-bar');
    progressBars.forEach(progressBar => {
        progressBar.style.opacity = "1";
    });
});

// remove file from dropzone when complete
myDropzone.on("complete", function(file) {
    myDropzone.removeFile(file);
});