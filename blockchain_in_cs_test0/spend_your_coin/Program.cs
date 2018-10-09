using System;
using QBitNinja.Client;


namespace spend_your_coin
{
    class Program
    {
        // set the bitcoin network, in this case it is testNet
        var network = Network.TestNet;
        var privateKey = new Key();

        // generate a private key
        var bitcoinPrivateKey = privateKey.GetWif(network);

        // get the bitcoin address
        var address = bitcoinPrivateKey.GetAddress();

        Console.WriteLine(bitcoinPrivateKey);
        Console.WriteLine(address);

        // spend bitcoin
        var bitcoinPrivateKey =
            new BitcoinSecret("import_your_private_key_here");
        var network = bitcoinPrivateKey.Network;
        var address = bitcoinPrivateKey.GetAddress();

        Console.WriteLine(bitcoinPrivateKey);
        Console.WriteLine(address);

        // get the transaction information
        var client = new QBitNinjaClient(network);
        var transactionId = uint256.Parse("your_transaction_ID_here");
        var transactionResponse = client.GetTransaction(transactionId).Result;

        Console.WriteLine(transactionResponse.TransactionId);
        Console.WriteLine(transactionResponse.Block.Confirmations);

        // spend the 2nd outpoint
        // from where? constructing the TxIn and adding it to the transaction
        var receivedCoins = transactionResponse.ReceivedCoins;
        OutPoint outPointToSpend = null;

        foreach (var coin in receivedCoins)
        {
            if (coin.TxOut.ScriptPubKey == bitcoinPrivateKey.ScriptPubKey)
            {
                outPointToSpend = coin.Outpoint;
            }
        }
        if(outPointToSpend == null)
            throw new Exception("TxOut doesn't contain our ScriptPubKey");
        Console.WriteLine("We want to spend {0}. outpoint:", outPointToSpend.N + 1);

        // payment - need to reference the outpoint in the transaction
        // create a transaction:
        var transaction = new Transaction();
        transaction.Input.Add(new TxIn()
        {
            PrevOut = outPointToSpend
        });

        // to where and how much?
        // construct the TxOut and add it to the transaction
        // 1 bitcoin (BTC) is 1,000,000 bits
        // 100 satoshi (sat) is 1 bit
        // 1 sat is the smallest unit on the bitcoin network
        
    }
}
