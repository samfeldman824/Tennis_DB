// import React, { useState } from 'react';
import Dropzone, { IDropzoneProps } from 'react-dropzone-uploader';
import 'react-dropzone-uploader/dist/styles.css';


export const DropzoneBox = () => {
    
    const handleChangeStatus: IDropzoneProps['onChangeStatus'] = ({ meta, file }, status) => {
        if (status === 'done') {
          console.log(`File ${meta.name} added`)
        } else if (status === 'preparing') {
            console.log(`File ${meta.name} being prepared`)
        } else if (status === 'removed') {
          console.log(`File ${meta.name} removed`)
        } else if (status === 'error_upload') {
          console.error(`Error uploading file ${meta.name}`)
        } else if (status === 'error_validation') {
          console.error(`Validation error for file ${meta.name}`)
        }
      }

    const getUploadParams: IDropzoneProps['getUploadParams'] = () => (
        { url: 'https://localhost:8080/' })
      

  return (
    <Dropzone
    getUploadParams={getUploadParams}
    onChangeStatus={handleChangeStatus}
    accept=".csv"
    inputContent="Drop CSV File"
    />
  );
};
