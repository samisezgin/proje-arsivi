package com.emlakcepte.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.emlakcepte.model.Search;
import com.emlakcepte.model.User;
import com.emlakcepte.repository.UserRepository;

@Service
public class UserService
{
	@Autowired
	private UserRepository userRepository /*= new UserRepository()*/;
	
	public UserService(UserRepository userRepository)
	{
		this.userRepository=userRepository;
	}
	public void createUser(User user)
	{
		//System.out.println(userDao);
		if (user.getPassword().length() < 8)
		{
			System.out.println("Password must be at least 8 characters!");
			return;
		}
		userRepository.createUser(user);
	}

	public List<User> getAllUsers()
	{
		System.out.println("getAllUsers()");
		return userRepository.getAllUsers();
	}

	public void printAllUsers()
	{
		
		getAllUsers().forEach(user -> System.out.println(user.getName()));
	}
	
	public void saveSearch(User user, Search search)
	{
		userRepository.saveSearch(user, search);
	}
}
