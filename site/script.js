
document.addEventListener('DOMContentLoaded', () => {
    const screens = document.querySelectorAll('.screen');
    const optionButtons = document.querySelectorAll('.option-button');
    const photoUpload = document.getElementById('photo_upload');
    const videoUpload = document.getElementById('video_upload');
    let currentScreen = 'main_menu';
    const uploadPlaceholders = document.querySelectorAll('.upload-placeholder[data-upload-target]');
    const cameraPreview = document.querySelector('.camera-preview');
     const processedCamera = document.querySelector("#classifier_emotion_camera .processed-camera");
    const backButtons = document.querySelectorAll('.back-button');
     let cameraStream = null;
    function showScreen(screenId) {
        screens.forEach(screen => {
            screen.classList.add('hidden');
             if (screen.id === screenId) {
               screen.classList.remove('hidden')
            }
        });
       
        currentScreen = screenId;
    }
   
  // Function to start the camera
   function startCamera(targetElement, showPreview=false) {
     navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
          cameraStream = stream;
          const videoElement = document.createElement('video');
          videoElement.srcObject = stream;
          videoElement.play();
          targetElement.innerHTML = '';
           if (showPreview){
             processedCamera.innerHTML = '';
            processedCamera.appendChild(videoElement);
             processCameraStream(videoElement)
           } else {
               targetElement.appendChild(videoElement);
           }
        })
        .catch(function (err) {
            console.error("Error accessing camera:", err);
           alert("Error accessing camera. Please check your permissions.");
        });
}

    optionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const action = button.getAttribute('data-action');
             if (action === "open_camera") {
                  showScreen('classifier_emotion_camera');
                 startCamera(processedCamera, true)
            }else {
               showScreen(action);
            }
        });
    });
  
   backButtons.forEach(button => {
      button.addEventListener('click', () => {
          showScreen('main_menu');
        if(currentScreen == "classifier_emotion_camera" && cameraStream){
              cameraStream.getTracks().forEach(track => track.stop());
                cameraStream = null;
         }
      });
   });

  uploadPlaceholders.forEach(placeholder => {
        placeholder.addEventListener('click', () => {
            const inputId = placeholder.getAttribute('data-upload-target');
            document.getElementById(inputId).click();
        });
    });
    function handleFileUpload(file, previewElement) {
        if (!file) return;

        if (file.type.startsWith('image')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                 previewElement.innerHTML = `<img src="${e.target.result}" />`;
                if (currentScreen === 'upload_photo') {
                     processImage(e.target.result, previewElement);
                }
                
            };
            reader.readAsDataURL(file);

        } else if (file.type.startsWith('video')) {
            const reader = new FileReader();
            reader.onload = (e) => {
               previewElement.innerHTML = `<video src="${e.target.result}" controls></video>`;
               if (currentScreen === 'upload_video') {
                     processVideo(e.target.result, previewElement);
                }
            }
             reader.readAsDataURL(file);
        }
    }

    photoUpload.addEventListener('change', (event) => {
      const file = event.target.files[0];
      const previewElement = document.querySelector('#upload_photo .image-preview');
      handleFileUpload(file, previewElement);
      
    });
  
  videoUpload.addEventListener('change', (event) => {
    const file = event.target.files[0];
      const previewElement = document.querySelector('#upload_video .video-preview');
      handleFileUpload(file, previewElement);
    });


    // --- Processing Logic Placeholder ---
    // Replace these functions with the actual logic to call your Python scripts
    function processImage(imageDataURL, previewElement) {
      
        showScreen('analyze_photo')
        const processedImage = document.querySelector('#analyze_photo .processed-image')
        processedImage.innerHTML = `<img src="${imageDataURL}" />`;

        // --- Placeholder to emulate Python script response
        setTimeout(() => {
             showScreen('classifier_emotion_img');
            document.querySelector("#classifier_emotion_img .processed-image").innerHTML = `<img src="${imageDataURL}" />`;
            document.getElementById('img_emotion_label').textContent = "Happy";
       }, 2000)
         // Example:
        // fetch('/process_image', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ image: imageDataURL })
        // })
        // .then(response => response.json())
        // .then(data => {
         // if (data.face_detected) {
            //   showScreen('classifier_emotion_img');
            //  document.querySelector("#classifier_emotion_img .processed-image").innerHTML = `<img src="${data.processed_image}" />`;
            //    document.getElementById('img_emotion_label').textContent = data.emotion;
            //} else {
            //   showScreen('no_human_in_photo')
            //  document.querySelector("#no_human_in_photo .image-preview").innerHTML = `<img src="${imageDataURL}" />`;
            //}
         // })
        // .catch(error => console.error('Error:', error));
    }
   function processVideo(videoDataURL, previewElement) {
     
        showScreen('analyze_video');
        const processedVideo = document.querySelector('#analyze_video .processed-video');
        processedVideo.innerHTML = `<video src="${videoDataURL}" controls></video>`;

        // --- Placeholder to emulate Python script response
      setTimeout(() => {
           showScreen('classifier_emotion_video');
            document.querySelector("#classifier_emotion_video .processed-video").innerHTML = `<video src="${videoDataURL}" controls></video>`;
            document.getElementById('video_emotion_label').textContent = "Neutral";
      }, 2000)
        // Example:
        // fetch('/process_video', {
        //   method: 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify({ video: videoDataURL })
        // })
       //.then(response => response.json())
       //.then(data => {
       //  if (data.face_detected) {
      //      showScreen('classifier_emotion_video');
      //       document.querySelector("#classifier_emotion_video .processed-video").innerHTML = `<video src="${data.processed_video}" controls></video>`;
        //   document.getElementById('video_emotion_label').textContent = data.emotion;
        // } else {
      //      showScreen('no_human_in_video')
       //     document.querySelector("#no_human_in_video .video-preview").innerHTML = `<video src="${videoDataURL}" controls></video>`;
      //  }
      // })
       // .catch(error => console.error('Error:', error));
    }
    
    function processCameraStream(videoElement) {
      
        let counter = 0;
        function analyzeFrame() {
              if (currentScreen !== 'classifier_emotion_camera') {
               return;
              }
         
          if (counter < 100){
          counter ++;
            
            const emotion = ["Happy", "Sad", "Neutral", "Angry", "Surprised"][Math.floor(Math.random() * 5)];
                document.getElementById('camera_emotion_label').textContent = emotion
              setTimeout(analyzeFrame, 300);
            }
        }
      analyzeFrame();

        // Example of API call, you need to implement the python
      /*  const canvas = document.createElement('canvas');
       const context = canvas.getContext('2d');

        function analyzeFrame() {
            if (currentScreen !== 'classifier_emotion_camera') {
                return; // Stop when user leaves the screen
            }

            canvas.width = videoElement.videoWidth;
            canvas.height = videoElement.videoHeight;
             context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
              const imageDataURL = canvas.toDataURL('image/jpeg');

            fetch('/process_camera_frame', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageDataURL })
            })
            .then(response => response.json())
            .then(data => {
              if (data.face_detected){
                  document.getElementById('camera_emotion_label').textContent = data.emotion;
                }
                setTimeout(analyzeFrame, 300)
           })
           .catch(error => console.error('Error:', error));
        }
      analyzeFrame();
*/
    }
});
