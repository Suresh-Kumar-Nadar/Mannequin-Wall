// src/CameraCapture.jsx
import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";

const videoConstraints = {
  width: 640,
  height: 480,
  facingMode: "user",
};

const CameraCapture = () => {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const [isSending, setIsSending] = useState(false);
  const [responseImage, setResponseImage] = useState(null);

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
    sendToBackend(imageSrc);
  };

  const sendToBackend = async (imageSrc) => {
    setIsSending(true);

    try {
      // Convert base64 to Blob
      const res = await fetch(imageSrc);
      const blob = await res.blob();

      const formData = new FormData();
      formData.append("source_image", blob, "source.jpg");

      // For testing, use the same image as target
      formData.append("target_image", blob, "target.jpg");
      formData.append("face_enhancer", "true");

      const result = await axios.post("http://localhost:5000/swap_faces", formData, {
        responseType: "blob",
      });

      const resultImageURL = URL.createObjectURL(result.data);
      setResponseImage(resultImageURL);
    } catch (err) {
      console.error("Error sending to backend:", err);
    }

    setIsSending(false);
  };

  return (
    <div>
      {!image && (
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={640}
          height={480}
          videoConstraints={videoConstraints}
        />
      )}
      <br />
      {!image && (
        <button onClick={capture} className="bg-blue-500 text-white px-4 py-2 rounded">
          Take Photo
        </button>
      )}
      {image && <img src={image} alt="Captured" className="mt-4" />}
      {isSending && <p>Processing...</p>}
      {responseImage && (
        <div className="mt-4">
          <h2>Processed Image:</h2>
          <img src={responseImage} alt="Processed" />
        </div>
      )}
    </div>
  );
};

export default CameraCapture;
