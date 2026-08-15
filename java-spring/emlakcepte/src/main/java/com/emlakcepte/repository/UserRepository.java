package com.emlakcepte.repository;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Component;

import com.emlakcepte.model.*;

@Component
public class UserRepository
{
	private static List<User> userList = new ArrayList<>();	
	
	
	public void createUser(User user)
	{
		userList.add(user);
	}

	public List<User> getAllUsers()
	{
		return userList;
	}
	
	public void saveSearch(User user, Search search)
	{
		user.getSearches().add(search);
	}
}
