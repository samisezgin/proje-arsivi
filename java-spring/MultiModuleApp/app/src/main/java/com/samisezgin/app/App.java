package com.samisezgin.app;

import com.samisezgin.core.HelloService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

/**
 * Hello world!
 */
@SpringBootApplication
@ComponentScan(basePackages = {"com.samisezgin.core", "com.samisezgin.app"})
//@PropertySource("classpath:/application-core.properties")
// core'daki application-core.properties dosyasını burada dahil ediyoruz
public class App implements CommandLineRunner {
    private final TestService testService;

    public App(TestService testService) {
        this.testService = testService;
    }

    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        System.out.println("Dosya var mı? " +
                App.class.getClassLoader().getResource("application-core.properties"));
        System.out.println(testService.getTestValue());
        System.out.println(testService.getabcValue());
        HelloService helloService = new HelloService();
        System.out.println(helloService.sayHello());
        System.out.println("Hello World!");
    }
}
