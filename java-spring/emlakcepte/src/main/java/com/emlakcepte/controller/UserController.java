package com.emlakcepte.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.emlakcepte.model.Search;
import com.emlakcepte.model.User;
import com.emlakcepte.service.UserService;

@RestController
@RequestMapping(value = "/users")
public class UserController
{
	@Autowired
	private UserService userService;
	
	public UserController (UserService userService)
	{
		this.userService = userService;
	}
	@GetMapping
	public List<User> getAll()
	{
		System.out.println("HTTP-GET UserController called.");
		return userService.getAllUsers();
	}

	@PostMapping("/create")
	public ResponseEntity<User> create(@RequestBody User user)
	{
		userService.createUser(user);
		System.out.println("HTTP-POST UserController -> Create User called.");
		return new ResponseEntity<>(user, HttpStatus.CREATED);
	}

	@PostMapping("/saveSearch")
	public ResponseEntity<Search> saveSearch(@RequestBody User user, @RequestBody Search search)
	{
		System.out.println("HTTP-POST UserController -> Save Search called.");
		userService.saveSearch(user, search);
		return new ResponseEntity<>(search, HttpStatus.ACCEPTED);
	}
}
