package com.emlakcepte.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.emlakcepte.client.model.Banner;
import com.emlakcepte.model.Realty;
import com.emlakcepte.service.RealtyService;

@RestController
@RequestMapping(value = "/realties")
public class RealtyController
{
	@Autowired
	private RealtyService realtyService;

	@GetMapping
	public ResponseEntity<List<Realty>> getAll()
	{
		System.out.println("HTTP-GET RealtyController getAll() called.");
		return new ResponseEntity<>(realtyService.getAll(), HttpStatus.OK);
	}
	
	@PostMapping
	public ResponseEntity<Banner> createRealty(Realty realty)
	{
		return new ResponseEntity<>(realtyService.createRealty(realty),HttpStatus.CREATED);
	}

}
