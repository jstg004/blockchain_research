using System;
using System.Collections.Generic;
using System.Linq;
using NBitcoin;
using QBitNinja.Client;

namespace Transaction
{
    class Program
    {
        static void Main()
        {
            // DO NOT  use the transaction ID to handle unconfirmed tranactions
            //    - the transaction ID can be manipulated before it is confirmed
            //    - transaction malleability

            // Create a client
            QBitNinjaClient client = new QBitNinjaClient(Network.Main);

            // parse transaction ID to NBitcoin.uint256 for the client
            // this transaction number is from the tutorial book
            // use QBitNinja.Client to get detailed information on transactions
            var transactionId = uint256.Parse(
                "f13dc48fb035bbf0a6e989a26b3ecb57b84f85e0836e777d6edf60d87a4a2d94");

            // Query the transaction
            // GetTransactionResponse contains the value and the scriptPubKey of
            //    the inputs being spent in the transaction
            QBitNinja.Client.Models.GetTransactionResponse transactionResponse =
                client.GetTransaction(transactionId).Result;
            NBitcoin.Transaction transaction = transactionResponse.Transaction;
            
            Console.WriteLine();
            Console.WriteLine();
            Console.WriteLine("QBitNinja transactionResponse.TransactionId: ");
            Console.WriteLine(transactionResponse.TransactionId);
            Console.WriteLine();
            Console.WriteLine("NBitcoin transaction.GetHash: ");
            Console.WriteLine(transaction.GetHash());
            Console.WriteLine("---------------------------------------");
            Console.WriteLine();

            // RECEIVED COINS
            // using QBitNinja.Client
            // there is 1 output sent to the ScriptPubKey
            List<ICoin> receivedCoins = transactionResponse.ReceivedCoins;

            foreach (Coin coin in receivedCoins)
            {
                Money amount = coin.Amount;
                Console.WriteLine("Found using QBitNinja.Client");
                Console.WriteLine("Amount of coins received: ");
                Console.WriteLine(amount.ToDecimal(MoneyUnit.BTC));

                var paymentScript = coin.ScriptPubKey;
                Console.WriteLine("ScriptPubKey: ");
                Console.WriteLine(paymentScript);

                var address = paymentScript.GetDestinationAddress(Network.Main);
                Console.WriteLine("Destination address on mainNet: ");
                Console.WriteLine(address);
                Console.WriteLine("---------------------------------------");
                Console.WriteLine();
            }

            // RECEIVED COINS
            // using NBitcoin - same information as using QBitNinja.Client
            var outputs = transaction.Outputs;

            foreach (TxOut output in outputs)
            {
                Coin coin = new Coin(transaction, output);
                Money amount = coin.Amount;
                Console.WriteLine("Found using NBitcoin");
                Console.WriteLine("Amount of coins received: ");
                Console.WriteLine(amount.ToDecimal(MoneyUnit.BTC));

                var paymentScript = coin.GetScriptCode();
                Console.WriteLine("ScriptPubKey: ");
                Console.WriteLine(paymentScript);

                var address = paymentScript.GetDestinationAddress(Network.Main);
                Console.WriteLine("Destination address on mainNet: ");
                Console.WriteLine(address);
                Console.WriteLine("---------------------------------------");
                Console.WriteLine();
            }

            // RECEIVED COINS
            // using NBitcoin - same information as using QBitNinja.Client
            foreach (TxOut output in outputs)
            {
                Money amount = output.Value;
                Console.WriteLine("Found using NBitcoin");
                Console.WriteLine("Amount of coins received: ");
                Console.WriteLine(amount.ToDecimal(MoneyUnit.BTC));

                var paymentScript = output.ScriptPubKey;
                Console.WriteLine("ScriptPubKey: ");
                Console.WriteLine(paymentScript);

                var address = paymentScript.GetDestinationAddress(Network.Main);
                Console.WriteLine("Destination address on mainNet: ");
                Console.WriteLine(address);
                Console.WriteLine("---------------------------------------");
                Console.WriteLine();
            }

            // SPENT COINS
            // using QBitNinja.Client
            List<ICoin> spentCoins = transactionResponse.SpentCoins;
            
            foreach (Coin coin in spentCoins)
            {
                Money amount = coin.Amount;
                Console.WriteLine("Found using QBitNinja.Client");
                Console.WriteLine("Amount of coins spent: ");
                Console.WriteLine(amount.ToDecimal(MoneyUnit.BTC));

                var paymentScript = coin.ScriptPubKey;
                Console.WriteLine("ScriptPubKey: ");
                Console.WriteLine(paymentScript);

                Console.WriteLine("Destination address on mainNet: ");
                var address = paymentScript.GetDestinationAddress(Network.Main);
                Console.WriteLine(address);
                Console.WriteLine("---------------------------------------");
                Console.WriteLine();
            }

            // SPENT COINS
            foreach (Coin coin in spentCoins)
            {
                // TxOut represents an amount of bitcoin and a ScriptPubLKey
                //    the ScriptPubLKey is the recipient
                TxOut previousOutput = coin.TxOut;
                Money amount = previousOutput.Value;
                Console.WriteLine("Amount of coins spent: ");
                Console.WriteLine(amount.ToDecimal(MoneyUnit.BTC));

                var paymentScript = previousOutput.ScriptPubKey;
                Console.WriteLine("ScriptPubKey: ");
                Console.WriteLine(paymentScript);

                var address = paymentScript.GetDestinationAddress(Network.Main);
                Console.WriteLine("Destination address on mainNet: ");
                Console.WriteLine(address);
                Console.WriteLine("---------------------------------------");
                Console.WriteLine();
            }

            // the difference between the inputs and outputs = transaction fees
            //    aka miner's fee
            var fee = transaction.GetFee(spentCoins.ToArray());
            Console.WriteLine("Fees spent in BTC: " + fee.ToDecimal(MoneyUnit.BTC));
            Console.WriteLine("---------------------------------------");
            Console.WriteLine();
            
            var inputs = transaction.Inputs;

            // previous output is referenced
            // each input contains the previous output which was spent to fund
            //    the current input
            // TxIn contains the Outpoint of the TxOut which is spent and it
            //    contains the ScriptSig
            // using the previous output's transaction ID - can get information
            //    associated with the transaction
            foreach (TxIn input in inputs)
            {
                OutPoint previousOutpoint = input.PrevOut;
                Console.WriteLine("Hash of the previous transaction: ");
                Console.WriteLine(previousOutpoint.Hash);
                Console.WriteLine("Index of the previous transaction: ");
                Console.WriteLine(previousOutpoint.N);
                Console.WriteLine("---------------------------------------");
                Console.WriteLine();
            }

            // create a transaction output with 21 bitcoin from the 1st ScriptPubKey
            //    in the current transaction
            Money twentyOneBtc = new Money(21, MoneyUnit.BTC);
            var scriptPubKey = transaction.Outputs.First().ScriptPubKey;
            TxOut txOut = new TxOut(twentyOneBtc, scriptPubKey);
            OutPoint firstOutPoint = spentCoins.First().Outpoint;

            Console.WriteLine("1st transaction hash: ");
            Console.WriteLine(firstOutPoint.Hash);
            Console.WriteLine("1st transaction index: ");
            Console.WriteLine(firstOutPoint.N);
            Console.WriteLine("Amount of inputs contained in the transaciton: ");
            Console.WriteLine(transaction.Inputs.Count);

            OutPoint firstPreviousOutPoint = transaction.Inputs.First().PrevOut;
            var firstPreviousTransactionResponse =
                client.GetTransaction(firstPreviousOutPoint.Hash).Result;

            // the coinbase transaction contains the original transaction which
            //    mined the bitcoin
            Console.WriteLine("Is this transaction the coinbase transaction?");
            Console.WriteLine(firstPreviousTransactionResponse.IsCoinbase);
            Console.WriteLine("---------------------------------------");
            Console.WriteLine();

            NBitcoin.Transaction firstPreviousTransaction =
                firstPreviousTransactionResponse.Transaction;

            // follow the ancestory trail of the transaction all the way to
            //    its origin (mined block)
            // the following code can take a very long time to run
            //    it traces the blockchain to find the origin coin
            //while (firstPreviousTransactionResponse.IsCoinbase == false)
            //{
            //    Console.WriteLine(firstPreviousTransaction.GetHash());

            //    firstPreviousOutPoint =
            //        firstPreviousTransaction.Inputs.First().PrevOut;
            //    firstPreviousTransactionResponse =
            //        client.GetTransaction(firstPreviousOutPoint.Hash).Result;
            //    firstPreviousTransaction =
            //        firstPreviousTransactionResponse.Transaction;
            //}

            // the coinbase transaction is the only transaction whose value of
            //    the output is larger than teh value of the input
            // the coinbase transaction is the 1st transaction of every block
            // consensus rules enforce this rule:
            //    the sum of output's value in the coinbase transaction does not
            //        exceed the sum of transaction fees in the block plus the
            //        mining reward
            Money spentAmount = Money.Zero;
            foreach (var spentCoin in spentCoins)
            {
                spentAmount = (Money)spentCoin.Amount.Add(spentAmount);
            }
            Console.WriteLine("Total amount spent: ");
            Console.WriteLine(spentAmount.ToDecimal(MoneyUnit.BTC));

            Money receivedAmount = Money.Zero;
            foreach (var receivedCoin in receivedCoins)
            {
                receivedAmount = (Money)receivedCoin.Amount.Add(receivedAmount);
            }
            Console.WriteLine("Total amount received: ");
            Console.WriteLine(receivedAmount.ToDecimal(MoneyUnit.BTC));

            Console.WriteLine("Total fees spent: ");
            Console.WriteLine(
                (spentAmount - receivedAmount).ToDecimal(MoneyUnit.BTC));
            Console.WriteLine("---------------------------------------");
            Console.WriteLine();

            //var inputs = transaction.Inputs;
            //foreach (TxIn input in inputs)
            //{
            //    uint256 previousTransactionId = input.PrevOut.Hash;
            //    GetTransactionResponse previousTransactionResponse =
            //        client.GetTransaction(previousTransactionId).Result;

            //    NBitcoin.Transaction previousTransaction =
            //        previousTransactionResponse.Transaction;

            //    var previousTransactionOutputs = previousTransaction.Outputs;
            //    foreach (TxOut previousTransactionOutput in previousTransactionOutputs)
            //    {
            //        Money amount = previousTransactionOutput.Value;

            //        Console.WriteLine(amount.ToDecimal(MoneyUnit.BTC));
            //        var paymentScript = previousTransactionOutput.ScriptPubKey;
            //        Console.WriteLine(paymentScript);  // It's the ScriptPubKey
            //        var address = paymentScript.GetDestinationAddress(Network.Main);
            //        Console.WriteLine(address);
            //        Console.WriteLine();
            //    }
            //}
        }
    }
}
