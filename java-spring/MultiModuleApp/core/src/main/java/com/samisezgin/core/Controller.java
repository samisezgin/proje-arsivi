package com.samisezgin.core;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/test")
public class Controller {
    @GetMapping("/{abc}")
    public void test(@PathVariable String abc) {
        System.out.println(abc);
    }
}
