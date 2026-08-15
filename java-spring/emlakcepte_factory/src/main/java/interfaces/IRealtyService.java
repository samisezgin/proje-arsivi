package interfaces;

import java.util.List;

import emlakcepte.model.Realty;
import emlakcepte.model.RealtyCategory;
import emlakcepte.model.User;

public interface IRealtyService
{
	public void createRealty(Realty realty);
	public List<Realty> getAll();
	public void printAll();
	public void printByProvince(String province);
	public void getAllByProvinceAndDistrict(String province, String district);
	public long getRealtyNumberInProvince(String province);
	public long getRealtyNumberInProvince(List<String> provinces);
	public long getHouseNumberInProvince(String province, RealtyCategory category);
	public void showCaseByProvince(String province);
	public List<Realty> getAllByUsername(User user);
	public void printAllByUsername(User user);
	public List<Realty> getAllByActive();
	public void printAllByActive();
}
