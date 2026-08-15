package com.samisezgin.emlakburada.services;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.samisezgin.emlakburada.model.User;
import com.samisezgin.emlakburada.repository.UserRepository;

@Service
public class UserService
{
	@Autowired
	private UserRepository userRepository;

	public List<User> getAll()
	{
		return userRepository.findAll();
	}

}
