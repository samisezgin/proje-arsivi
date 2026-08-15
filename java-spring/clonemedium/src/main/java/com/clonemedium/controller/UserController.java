package com.clonemedium.controller;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.clonemedium.model.User;
import com.clonemedium.services.UserService;

@RestController
@RequestMapping("/users")
public class UserController
{
	@Autowired
	private UserService userService;

	@GetMapping
	public List<User> getAll()
	{
		return userService.getAll();
	}

	@PostMapping
	public User create(User user)
	{
		userService.createUser(user);
		return user;
	}

	@PutMapping
	public User update(String userName, User user)
	{

		User tempUser = userService.getAll().stream().filter(usr -> usr.getUserName().equals(user.getUserName()))
				.findFirst().get();
		userService.getAll().remove(tempUser);
		userService.getAll().add(user);
		return user;
	}
	
	

}
