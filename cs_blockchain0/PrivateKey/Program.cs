using System;
using NBitcoin;


namespace PrivateKey
{
    class Program
    {
        static void Main()
        {
            // private key - represented by Base58Check - Bitcoin Secret
            //    - Wallet Import Format (WIF)
            Key privateKey = new Key(); // generates a random private key

            // generates Bitcoin secret (WIF) from the private key in mainNet
            BitcoinSecret mainNetPrivateKey =
                privateKey.GetBitcoinSecret(Network.Main);
            
             // generates Bitcoin secret (WIF) from the private key in testnNet
            BitcoinSecret testNetPrivateKey =
                privateKey.GetBitcoinSecret(Network.TestNet);

            Console.WriteLine("mainNet privateKey: ");
            Console.WriteLine(mainNetPrivateKey);
            Console.WriteLine("testNet privateKey: ");
            Console.WriteLine(testNetPrivateKey);

            bool WifIsBitcoinSecret =
                mainNetPrivateKey == privateKey.GetWif(Network.Main);
            
            Console.WriteLine("Is the bitcoin mainNet secret same as WiF? ");
            Console.WriteLine(WifIsBitcoinSecret);

            // can go from bitcoin secret to the private key
            // it is impossible to go from the bitcoin address to the public key
            //    - the bitcoin address contains only a hash of the public key
            BitcoinSecret bitcoinPrivateKey = privateKey.GetWif(Network.Main);

            Console.WriteLine("WiF: " + bitcoinPrivateKey);
            
            Key samePrivateKey = bitcoinPrivateKey.PrivateKey;
            PubKey publicKey = privateKey.PubKey;

            Console.WriteLine("publicKey: " + publicKey);

            BitcoinPubKeyAddress bitcoinPubicKey =
                publicKey.GetAddress(Network.Main);

            Console.WriteLine("Bitcoin mainNet public key address: " +
                bitcoinPubicKey);
        }
    }
}
