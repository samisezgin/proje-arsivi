package com.example.fileuploader;

import java.io.Serializable;

public class SafeFile implements Serializable{
    private String fileName;
    private byte[] fileByteArray;

    public SafeFile() {
    }

    public byte[] getFileByteArray() {
        return fileByteArray;
    }

    public void setFileByteArray(byte[] fileByteArray) {
        this.fileByteArray = fileByteArray;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

}
