package interfaces;

import java.util.List;

import emlakcepte.model.Search;
import emlakcepte.model.User;

public interface IUserService
{
	public void createUser(User user);
	public List<User> getAllUsers();
	public void printAllUsers();
	public void saveSearch(User user, Search search);
}
