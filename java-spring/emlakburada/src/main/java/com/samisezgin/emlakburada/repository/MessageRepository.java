package com.samisezgin.emlakburada.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.samisezgin.emlakburada.model.Message;

public interface MessageRepository extends JpaRepository<Message, Long>
{
	Message findByTitle(String title);

	Message findById(Integer id);
}