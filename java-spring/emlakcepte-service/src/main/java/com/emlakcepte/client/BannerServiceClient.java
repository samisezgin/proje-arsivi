package com.emlakcepte.client;

import org.springframework.http.HttpEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.client.RestTemplate;

import com.emlakcepte.client.model.Banner;


@Service
//@FeignClient(value ="emlakcepte-banner-service", url="{server.port}")
public class BannerServiceClient
{
	//@PostMapping(value="/banners")
	//Banner create(@RequestBody Banner banner);
	public void create(Banner banner)
	{
		String url="http://localhost:8081/banners";
		RestTemplate template=new RestTemplate();
		HttpEntity<Banner> request=new HttpEntity<>(banner);
		template.postForObject(url, request, Banner.class);
		
	}
}
