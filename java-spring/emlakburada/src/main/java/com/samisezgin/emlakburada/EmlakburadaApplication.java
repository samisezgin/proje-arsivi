package com.samisezgin.emlakburada;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import com.samisezgin.emlakburada.model.Message;
import com.samisezgin.emlakburada.model.User;
import com.samisezgin.emlakburada.repository.MessageRepository;
import com.samisezgin.emlakburada.repository.UserRepository;

@SpringBootApplication
public class EmlakburadaApplication
{

	private static final Logger log = LoggerFactory.getLogger(EmlakburadaApplication.class);

	public static void main(String[] args)
	{
		SpringApplication.run(EmlakburadaApplication.class, args);

	}

	@Bean
	CommandLineRunner demoUser(UserRepository repository)
	{
		return (args) ->
		{
			// save a few customers
			repository.save(new User("Jack", "Bauer"));
			repository.save(new User("Chloe", "O'Brian"));
			repository.save(new User("Kim", "Bauer"));
			repository.save(new User("David", "Palmer"));
			repository.save(new User("Michelle", "Dessler"));

			// fetch all customers
			log.info("Customers found with findAll():");
			log.info("-------------------------------");
			for (User customer : repository.findAll())
			{
				log.info(customer.toString());
			}
			log.info("");

			// fetch an individual customer by ID
			User customer = repository.findById(1);
			log.info("Customer found with findById(1):");
			log.info("--------------------------------");
			log.info(customer.toString());
			log.info("");

			// fetch customers by last name
			log.info("Customer found with findByLastName('Bauer'):");
			log.info("--------------------------------------------");
			repository.findByLastName("Bauer").forEach(bauer ->
			{
				log.info(bauer.toString());
			});
			// for (Customer bauer : repository.findByLastName("Bauer")) {
			// log.info(bauer.toString());
			// }
			log.info("");
		};
	}

	@Bean
	CommandLineRunner demoMessage(MessageRepository repository, UserRepository uRepository)
	{
		return (args) ->
		{
			// save a few customers
			User user1 = uRepository.findById(1);
			User user2 = uRepository.findById(2);
			User user3 = uRepository.findById(3);
			User user4 = uRepository.findById(4);
			User user5 = uRepository.findById(5);

			System.out.println(user1.toString());
			System.out.println(user2.toString());
			// User user1 = new User("test1", "user1");
			// User user2 = new User("test2", "test2");
			Message message1 = new Message("title1", "content1", user2, user3);
			Message message2 = new Message("title2", "content2", user1, user3);
			
			
			repository.save(message1);			
			repository.save(message2);	
			
			message1.setFrom(user1);
			
			
			
			/*repository.save(new Message("title1", "content1", user1, user2));
			repository.save(new Message("title2", "content2", user2, user3));
			repository.save(new Message("title3", "content3", user3, user4));
			repository.save(new Message("title4", "content4", user4, user5));
			repository.save(new Message("title5", "content5", user5, user4));
			repository.save(new Message("title6", "content6", user4, user3));
			repository.save(new Message("title7", "content7", user3, user2));
			repository.save(new Message("title8", "content8", user2, user1));
			repository.save(new Message("title9", "content9", user1, user3));
			repository.save(new Message("title10", "content10", user1, user4));*/

			// fetch all customers
			log.info("Messages found with findAll():");
			log.info("-------------------------------");
			for (Message message : repository.findAll())
			{
				log.info(message.toString());
			}
			log.info("");

			// fetch an individual customer by ID
			/*Message message = repository.findByTitle("title1");
			log.info("Message found with findById(title):");
			log.info("--------------------------------");
			log.info(message.toString());
			log.info("");*/
		};
	}

}
