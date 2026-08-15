package com.samisezgin.emlakburada.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import com.samisezgin.emlakburada.model.User;
import com.samisezgin.emlakburada.services.UserService;

@Controller
@RequestMapping("/users")
public class UserController
{
	@Autowired
	private UserService userService;

	@GetMapping
	public ResponseEntity<List<User>> getAll()
	{
		return new ResponseEntity<>(userService.getAll(), HttpStatus.OK);
	}
}