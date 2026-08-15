package com.emlakcepte;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.ImportAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.cloud.openfeign.FeignAutoConfiguration;

@SpringBootApplication
@EnableFeignClients
@ImportAutoConfiguration({ FeignAutoConfiguration.class })
public class EmlakCepteMainApplication
{
	public static void main(String[] args)
	{
		
		SpringApplication.run(EmlakCepteMainApplication.class, args);

		/*
		 * UserService userService = new UserService(); RealtyService realtyService =
		 * new RealtyService();
		 * 
		 * User user1 = prepareUser("User1", "user1@hotmail.com", "user1pass");
		 * user1.setUserType(UserType.INDIVIDUAL); user1.setRealtyList(new
		 * ArrayList<>()); user1.setSearches(new ArrayList<>());
		 * 
		 * User user2 = prepareUser("USer2", "user2@hotmail.com", "user2pass");
		 * user2.setUserType(UserType.CORPORATE); user2.setRealtyList(new
		 * ArrayList<>());
		 * 
		 * userService.createUser(user1); userService.createUser(user2);
		 * 
		 * userService.printAllUsers();
		 * 
		 * Realty r1 = new Realty(); r1.setProvince("istanbul");
		 * r1.setDistrict("maltepe"); r1.setTitle("Lorem ipsum dolor sit amet1");
		 * r1.setRealtyType(RealtyType.HOUSE); r1.setUser(user1);
		 * r1.setCategory(RealtyCategory.SALE);
		 * 
		 * Realty r2 = new Realty(); r2.setProvince("ankara");
		 * r2.setDistrict("etimesgut"); r2.setTitle("Lorem ipsum dolor sit amet2");
		 * r2.setRealtyType(RealtyType.HOUSE); r2.setUser(user2);
		 * r2.setCategory(RealtyCategory.SALE);
		 * 
		 * Realty r3 = new Realty(); r3.setProvince("izmir"); r3.setDistrict("bergama");
		 * r3.setTitle("Lorem ipsum dolor sit amet3");
		 * r3.setRealtyType(RealtyType.HOUSE); r3.setUser(user2);
		 * r3.setCategory(RealtyCategory.SALE);
		 * 
		 * realtyService.createRealty(r1); realtyService.createRealty(r1);
		 * realtyService.createRealty(r1); realtyService.createRealty(r1);
		 * realtyService.createRealty(r2); realtyService.createRealty(r3);
		 * 
		 * System.out.println("Size: " + user1.getRealtyList().size());
		 * 
		 * realtyService.getAllByProvinceAndDistrict("istanbul", "maltepe");
		 * 
		 * System.out.println(
		 * "---------------------------------------------------------");
		 * 
		 * System.out.println("Istanbul total: " +
		 * realtyService.getRealtyNumberInProvince("istanbul"));
		 * 
		 * System.out.println(
		 * "---------------------------------------------------------");
		 * 
		 * System.out.println(realtyService.getHouseNumberInProvince("istanbul",
		 * RealtyCategory.SALE));
		 * 
		 * System.out.println(
		 * "-----------------------SHOWCASE----------------------------------");
		 * 
		 * realtyService.showCaseByProvince("istanbul");
		 * 
		 * System.out.println(
		 * "---------------------------------------------------------------");
		 * System.out.println(r1.getUser().getUserType());
		 * 
		 * System.out.println("Total izmir ankara istanbul : " +
		 * realtyService.getRealtyNumberInProvince(List.of("istanbul", "ankara",
		 * "izmir")));
		 * 
		 * System.out.println("-------------------------------------------------------")
		 * ;
		 * 
		 * Search search1 = new Search(); search1.setProvince("istanbul");
		 * search1.setDistrict("maltepe");
		 * 
		 * Search search2 = new Search(); search2.setProvince("ankara");
		 * search2.setDistrict("kizilay");
		 * 
		 * userService.saveSearch(user1, search1); userService.saveSearch(user1,
		 * search2);
		 * 
		 * List<Search> searches = user1.getSearches();
		 * 
		 * for (Search el : searches) { System.out.println(el); }
		 */

	}
	/*
	 * private static User prepareUser(String name, String email, String password) {
	 * User user = new User(); user.setName(name); user.setEmail(email);
	 * user.setPassword(password); user.setUserType(UserType.INDIVIDUAL);
	 * user.setCreateDate(LocalDateTime.now()); return user; }
	 */

	/*@Bean
	UserService userService()
	{
		return new UserService();
	}*/
	/*@Bean
	UserRepository userRepository()
	{
		return new UserRepository();
	}*/
	
	/*@Bean
	RealtyService realtyService()
	{
		return new RealtyService();
	}*/
	/*@Bean
	RealtyRepository realtyRepository()
	{
		return new RealtyRepository();
	}*/
}
