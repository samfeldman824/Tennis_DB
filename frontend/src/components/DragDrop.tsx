import { useState, useRef, DragEvent } from "react";
import Papa from "papaparse";

const DragDrop = () => {  
  // send files to the server // learn from my other video
  const fileToBlob = (file: any) => {
    return new Promise<Blob>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const blob = new Blob([reader.result as ArrayBuffer], { type: file.type });
        resolve(blob);
      };
      reader.onerror = reject;
      reader.readAsArrayBuffer(file);
    });
  };
  

  const handleUpload = async (event:any) => {
    const file = event.target.files[0];
    const blob = await fileToBlob(file)
    // const reader = new FileReader();
    // reader.readAsText(file);
    // reader.onload = () => {
    //   const csvData = Papa.parse(reader.result).data;
    //   console.log(csvData);
    // };

    // const reader = new FileReader();
    
    // reader.readAsText(file);
    // reader.onload = () => {
    //   const csvData = reader.result
    //   console.log(csvData)
    // };
    

    const formData = new FormData();
    formData.append('file', blob)
    const options_post = { method: 'POST', body: formData}
    const url = 'http://localhost:8080/matches/add_match/upload_csv'
    const data = await fetch(url, options_post)
    const json = await data.json()
    console.log(json.message)


    
  };

  // if (files) {
  //   return (
  //     <div className="uploads">
  //         <ul>
  //             {Array.from(files).map((file, idx) => <li key={idx}>{file.name}</li> )}
  //         </ul>
  //         <div className="actions">
  //             <button onClick={() => setFiles(null)}>Cancel</button>
  //             <button onClick={handleUpload}>Upload</button>
  //         </div>
  //     </div>
  //   );
  // }

  // console.log(files);
  return (
    <>
        <div 
            className="dropzone"
        >
          <h1>Drag and Drop Files to Upload</h1>
          <h1>Or</h1>
          <input type="file" onChange={handleUpload} />
          {/* <button onClick={() => inputRef.current?.click()}>Select Files</button> */}
        </div>
    </>
  );
};

export default DragDrop;
