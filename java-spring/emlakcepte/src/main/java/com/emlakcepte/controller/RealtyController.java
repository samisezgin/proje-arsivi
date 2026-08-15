package com.emlakcepte.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import com.emlakcepte.model.Realty;
import com.emlakcepte.model.RealtyCategory;
import com.emlakcepte.service.RealtyService;

//@RestController
//@RequestMapping(value = "/realties")
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

	@GetMapping(value = "/{province}/{district}")
	public ResponseEntity<List<Realty>> getByProvinceAndDistrict(@PathVariable String province,
			@PathVariable String district)
	{
		System.out.println("HTTP-GET RealtyController getByProvinceAndDistrict() called.");

		return new ResponseEntity<>(realtyService.getAllByProvinceAndDistrict(province, district), HttpStatus.OK);
	}

	@GetMapping(value = "/showcase/{province}")
	public ResponseEntity<List<Realty>> showCaseByProvince(@PathVariable String province)
	{
		System.out.println("HTTP-GET RealtyController showCaseByProvince() called.");
		return new ResponseEntity<>(realtyService.showCaseByProvince(province), HttpStatus.OK);
	}

	@GetMapping(value = "/count/{province}")
	public ResponseEntity<Long> getRealtyNumberInProvince(@PathVariable String province)
	{
		System.out.println("HTTP-GET RealtyController getRealtyNumberInProvince() called.");
		return new ResponseEntity<>(realtyService.getRealtyNumberInProvince(province), HttpStatus.OK);
	}

	@GetMapping(value = "/count/{province}/{category}")
	public ResponseEntity<Long> getHouseNumberInProvince(@PathVariable String province,
			@PathVariable RealtyCategory category)
	{
		System.out.println("HTTP-GET RealtyController getHouseNumberInProvince() called.");
		return new ResponseEntity<>(realtyService.getHouseNumberInProvince(province, category), HttpStatus.OK);
	}

}
