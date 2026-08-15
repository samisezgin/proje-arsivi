import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: "0.8.19",
  networks:{
    hardhat:{
      forking:{
        // Arsivlenirken anahtar ortam degiskenine tasindi; dosyada aciktaydi.
        // Kullanim: ALCHEMY_URL=https://eth-mainnet.g.alchemy.com/v2/<anahtar>
        url: process.env.ALCHEMY_URL ?? ""
      }
    }
  }
};

export default config;
