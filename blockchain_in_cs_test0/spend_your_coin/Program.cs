using System;
using QBitNinja.Client;


namespace spend_your_coin
{
    class Program
    {
        var network = Network.TestNet;

        var privateKey = new Key();
        var bitcoinPrivateKey = privateKey.GetWif(network);
        var address = bitcoinPrivateKey.GetAddress();

        Console.WriteLine(bitcoinPrivateKey);
        Console.WriteLine(address);

        var receivedCoins = transactionResponse.ReceivedCoins;
        OutPoint outPointToSpend = null;
        
    }
}
