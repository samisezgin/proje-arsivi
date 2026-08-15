package com.samisezgin.app;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class TestService {

    @Value("${test}")
    private String testValue;

    @Value("${abc}")
    private String abcValue;

    public String getTestValue() {
        return testValue;
    }

    public String getabcValue() {
        return abcValue;
    }
}