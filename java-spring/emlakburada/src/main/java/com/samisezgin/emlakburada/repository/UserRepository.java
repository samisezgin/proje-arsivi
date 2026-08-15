package com.samisezgin.emlakburada.repository;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

import com.samisezgin.emlakburada.model.User;

public interface UserRepository extends JpaRepository<User, Long>
{
	List<User> findByLastName(String lastName);

	public User findById(long id);

	//List<User> getAll();
}

