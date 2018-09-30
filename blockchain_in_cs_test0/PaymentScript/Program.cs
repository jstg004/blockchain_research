using System;
using NBitcoin;


namespace PaymentScript
{
    class Program
    {
        static void Main()
        {
            var publicKeyHash =
                new KeyId("14836dbe7f38c5ac3d49e8d790af808a4ee9edcf");

            var testNetAddress = publicKeyHash.GetAddress(Network.TestNet);
            var mainNetAddress = publicKeyHash.GetAddress(Network.Main);

            // bitcoin protocol identifies the recipient of the bitcoin by
            //    ScriptPubKey
            //    - this is a script that explains what condition must be met to
            //      claim ownership of the bitcoin(s)
            //    - the ScriptPubKey can be generated from the bitcoin address
            // the bitcoin address is human readable while the ScriptPubKey is
            //   blockchain readable
            Console.WriteLine("ScriptPubKey for bitcoin mainNet: " +
                mainNetAddress.ScriptPubKey);
            Console.WriteLine("ScriptPubKey for testNet: " +
                testNetAddress.ScriptPubKey);

            // can retrieve the hash from the ScriptPubKey
            // can generate a bitcoin address from the retrieved hash
            var paymentScript = publicKeyHash.ScriptPubKey;
            var sameMainNetAddress =
                paymentScript.GetDestinationAddress(Network.Main);
            Console.WriteLine(
                "Is mainNetAddress same as address dirived from ScriptPubKey");
            Console.WriteLine(mainNetAddress == sameMainNetAddress);

            // can retrieve the hash from the ScriptPubKey
            // can generate a bitcoin address from the retrieved hash
            var samePublicKeyHash = (KeyId)paymentScript.GetDestination();
            Console.WriteLine(
                "Does publicKeyHash match the hash from ScriptPubKey?");
            Console.WriteLine(publicKeyHash == samePublicKeyHash);
            var sameMainNetAddress2 =
                new BitcoinPubKeyAddress(samePublicKeyHash, Network.Main);
            Console.WriteLine(
                "Is mainNetAddress same as address dirived from " +
                "BitcoinPubKeyAddress?");
            Console.WriteLine(mainNetAddress == sameMainNetAddress2);
        }
    }
}