import unittest
from bal.transaction import *
from bal.wallet import generate_private_key
import copy


class TestTransactionMethods(unittest.TestCase):

    # HELPER METHODS

    # Returns [valid_tx, valid_unspent_tx_outs]
    def create_valid_transaction_kit(self):
        # Create valid transaction
        private_key = generate_private_key()
        public_key = private_key.get_verifying_key().to_der().encode('hex')
        example_new_tx_in_1 = new_tx_in(
            "testId270", 0, "testSignature")  # Signature will be updated
        example_new_tx_in_2 = new_tx_in(
            "testId271", 1, "testSignature")  # Signature will be updated
        example_new_tx_ins = [example_new_tx_in_1, example_new_tx_in_2]
        example_new_tx_out_1 = new_tx_out(
            "A61B5BE06CD7FE6D95064DAC98C97C9C8D128BEFACF7EA655D4EDF5B09B7DFAB6D059DD0A64B8C3CE9A11FEDC38143819BDF9CD4BC23EDCECFBAEB7DECACC81FE84CA7DE4AD33C89C9E848A5A8E8BDFD3BEA7BB3C4F81B4D",
            500)
        example_new_tx_out_2 = new_tx_out(
            "561B5BE06CD7FE6D95064DAC98C97C9C8D128BEFACF7EA655D4EDF5B09B7DFAB6D059DD0A64B8C3CE9A11FEDC38143819BDF9CD4BC23EDCECFBAEB7DECACC81FE84CA7DE4AD33C89C9E848A5A8E8BDFD3BEA7BB3C4F81B4D",
            501)
        example_new_tx_outs = [example_new_tx_out_1, example_new_tx_out_2]
        example_new_transaction = new_transaction(
            "testId28", example_new_tx_ins, example_new_tx_outs)
        example_get_transaction_id = get_transaction_id(
            example_new_transaction)
        example_new_transaction['id'] = example_get_transaction_id
        example_new_unspent_tx_out_1 = new_unspent_tx_out(
            "testId270", 0, public_key, 500)
        example_new_unspent_tx_out_2 = new_unspent_tx_out(
            "testId271", 1, public_key, 501)
        example_a_unspent_tx_outs = [
            example_new_unspent_tx_out_1,
            example_new_unspent_tx_out_2]
        private_key = private_key.to_der().encode(
            'hex')  # Create hex encoded private_key
        signature = sign_tx_in(
            example_new_transaction,
            0,
            private_key,
            example_a_unspent_tx_outs)  # Sign tx_ins
        # Update the signature
        example_new_transaction['tx_ins'][0]['signature'] = signature
        # Update the signature
        example_new_transaction['tx_ins'][1]['signature'] = signature

        return [example_new_transaction, example_a_unspent_tx_outs]

    # TEST METHODS

    def test_new_unspent_tx_out(self):

        example_new_unspent_tx_out = new_unspent_tx_out(
            "testId27", 0, "testAddress66", 500)
        intended_result = {
            'tx_out_id': 'testId27',
            'tx_out_index': 0,
            'address': 'testAddress66',
            'amount': 500}
        self.assertEqual(intended_result, example_new_unspent_tx_out)

    def test_new_tx_in(self):

        example_new_tx_in = new_tx_in("testId27", 0, "testSignature76")

        intended_result = {
            'tx_out_id': 'testId27',
            'tx_out_index': 0,
            'signature': 'testSignature76'}

        self.assertEqual(intended_result, example_new_tx_in)

    def test_new_tx_out(self):

        example_new_tx_out = new_tx_out("testAddress66", 500)

        intended_result = {'address': 'testAddress66', 'amount': 500}

        self.assertEqual(intended_result, example_new_tx_out)

    def test_new_transaction(self):
        example_new_tx_in_1 = new_tx_in("testId270", 0, "testSignature760")
        example_new_tx_in_2 = new_tx_in("testId271", 1, "testSignature761")
        example_new_tx_ins = [example_new_tx_in_1, example_new_tx_in_2]
        example_new_tx_out_1 = new_tx_out("testAddress660", 500)
        example_new_tx_out_2 = new_tx_out("testAddress661", 501)
        example_new_tx_outs = [example_new_tx_out_1, example_new_tx_out_2]
        example_new_transaction = new_transaction(
            "testId28", example_new_tx_ins, example_new_tx_outs)

        intended_result = {'id': 'testId28',
                           'tx_ins': [{'tx_out_id': 'testId270',
                                       'tx_out_index': 0,
                                       'signature': 'testSignature760'},
                                      {'tx_out_id': 'testId271',
                                       'tx_out_index': 1,
                                       'signature': 'testSignature761'}],
                           'tx_outs': [{'address': 'testAddress660',
                                        'amount': 500},
                                       {'address': 'testAddress661',
                                        'amount': 501}]}

        self.assertEqual(intended_result,
                         example_new_transaction)

    def test_get_transaction_id(self):
        example_new_tx_in_1 = new_tx_in("testId270", 0, "testSignature760")
        example_new_tx_in_2 = new_tx_in("testId271", 1, "testSignature761")
        example_new_tx_ins = [example_new_tx_in_1, example_new_tx_in_2]
        example_new_tx_out_1 = new_tx_out("testAddress660", 500)
        example_new_tx_out_2 = new_tx_out("testAddress661", 501)
        example_new_tx_outs = [example_new_tx_out_1, example_new_tx_out_2]
        example_new_transaction = new_transaction(
            "testId28", example_new_tx_ins, example_new_tx_outs)
        example_get_transaction_id = get_transaction_id(
            example_new_transaction)

        intended_result = "498d1fd4386ac8f5c0dcf6cda9154f901df632021b7fc11c9ab4398535fc9dd2"

        self.assertEqual(intended_result,
                         example_get_transaction_id)

    def test_is_valid_tx_in_structure(self):
        example_new_tx_in_1 = new_tx_in("testId270", 0, "testSignature760")
        example_is_valid_tx_in_structure = is_valid_tx_in_structure(
            example_new_tx_in_1)

        self.assertEqual(True, example_is_valid_tx_in_structure)

    def test_is_valid_tx_out_structure(self):
        example_new_tx_out_1 = new_tx_out(
            "A61B5BE06CD7FE6D95064DAC98C97C9C8D128BEFACF7EA655D4EDF5B09B7DFAB6D059DD0A64B8C3CE9A11FEDC38143819BDF9CD4BC23EDCECFBAEB7DECACC81FE84CA7DE4AD33C89C9E848A5A8E8BDFD3BEA7BB3C4F81B4D",
            500)
        example_is_valid_tx_out_structure = is_valid_tx_out_structure(
            example_new_tx_out_1)

        self.assertEqual(True, example_is_valid_tx_out_structure)

    def test_is_valid_transaction_structure(self):
        example_new_tx_in_1 = new_tx_in("testId270", 0, "testSignature760")
        example_new_tx_in_2 = new_tx_in("testId271", 1, "testSignature761")
        example_new_tx_ins = [example_new_tx_in_1, example_new_tx_in_2]
        example_new_tx_out_1 = new_tx_out(
            "A61B5BE06CD7FE6D95064DAC98C97C9C8D128BEFACF7EA655D4EDF5B09B7DFAB6D059DD0A64B8C3CE9A11FEDC38143819BDF9CD4BC23EDCECFBAEB7DECACC81FE84CA7DE4AD33C89C9E848A5A8E8BDFD3BEA7BB3C4F81B4D",
            500)
        example_new_tx_out_2 = new_tx_out(
            "561B5BE06CD7FE6D95064DAC98C97C9C8D128BEFACF7EA655D4EDF5B09B7DFAB6D059DD0A64B8C3CE9A11FEDC38143819BDF9CD4BC23EDCECFBAEB7DECACC81FE84CA7DE4AD33C89C9E848A5A8E8BDFD3BEA7BB3C4F81B4D",
            501)
        example_new_tx_outs = [example_new_tx_out_1, example_new_tx_out_2]
        example_new_transaction = new_transaction(
            "testId28", example_new_tx_ins, example_new_tx_outs)
        example_is_valid_transaction_strucure = is_valid_transaction_structure(
            example_new_transaction)

        self.assertEqual(True, example_is_valid_transaction_strucure)

    def test_validate_transaction(self):

        # Create valid transaction
        example_new_transaction_kit = self.create_valid_transaction_kit()
        example_new_transaction = example_new_transaction_kit[0]
        example_a_unspent_tx_outs = example_new_transaction_kit[1]
        example_validate_transaction = validate_transaction(
            example_new_transaction, example_a_unspent_tx_outs)

        # Test valid transaction
        self.assertEqual(True, example_validate_transaction)

        # Test invalid transaction structure

        example_new_transaction_2 = copy.deepcopy(example_new_transaction)
        example_new_transaction_2['tx_ins'][0]['tx_out_index'] = "this is invalid structure"
        example_validate_transaction = validate_transaction(
            example_new_transaction_2, example_a_unspent_tx_outs)
        self.assertEqual(False, example_validate_transaction)

        # Test invalid transaction id
        example_new_transaction_2 = copy.deepcopy(example_new_transaction)
        example_new_transaction_2['id'] = "this is invalid id"
        example_validate_transaction = validate_transaction(
            example_new_transaction_2, example_a_unspent_tx_outs)
        self.assertEqual(False, example_validate_transaction)

        # Test invalid tx_in
        example_new_transaction_2 = copy.deepcopy(example_new_transaction)
        example_a_unspent_tx_outs_2 = copy.deepcopy(example_a_unspent_tx_outs)
        example_a_unspent_tx_outs_2[0]['tx_out_index'] = 2
        example_validate_transaction = validate_transaction(
            example_new_transaction_2, example_a_unspent_tx_outs_2)
        self.assertEqual(False, example_validate_transaction)

        # Test not matching tx_in and tx_out total values
        example_new_transaction_2 = copy.deepcopy(example_new_transaction)
        example_a_unspent_tx_outs_2 = copy.deepcopy(example_a_unspent_tx_outs)
        example_a_unspent_tx_outs_2[0]['amount'] = 0
        example_validate_transaction = validate_transaction(
            example_new_transaction_2, example_a_unspent_tx_outs_2)
        self.assertEqual(False, example_validate_transaction)

    def test_new_coinbase_transaction(self):
        example_address = "A61B5BE06CD7FE6D95064DAC98C97C9C8D128BEFACF7EA655D4EDF5B09B7DFAB6D059DD0A64B8C3CE9A11FEDC38143819BDF9CD4BC23EDCECFBAEB7DECACC81FE84CA7DE4AD33C89C9E848A5A8E8BDFD3BEA7BB3C4F81B4D"
        example_block_index = 5
        example_tx_in = new_tx_in('', example_block_index, '')
        example_tx = new_transaction(
            None, [example_tx_in], [
                new_tx_out(
                    example_address, COINBASE_AMOUNT)])
        example_tx['id'] = get_transaction_id(example_tx)

        example_new_coinbase_transaction = new_coinbase_transaction(
            example_address, example_block_index)
        self.assertEqual(example_tx, example_new_coinbase_transaction)

    def test_validate_coinbase_tx(self):
        # Creating a valid coinbase_tx
        example_address = "A61B5BE06CD7FE6D95064DAC98C97C9C8D128BEFACF7EA655D4EDF5B09B7DFAB6D059DD0A64B8C3CE9A11FEDC38143819BDF9CD4BC23EDCECFBAEB7DECACC81FE84CA7DE4AD33C89C9E848A5A8E8BDFD3BEA7BB3C4F81B4D"
        example_block_index = 1
        example_new_coinbase_transaction = new_coinbase_transaction(
            example_address, example_block_index)

        # Test valid coinbase_tx
        example_validate_coinbase_tx = validate_coinbase_tx(
            example_new_coinbase_transaction, example_block_index)
        self.assertEqual(True, example_validate_coinbase_tx)

        # Test invalid id
        example_new_coinbase_transaction_2 = copy.deepcopy(
            example_new_coinbase_transaction)
        example_new_coinbase_transaction_2['id'] = "invalid_id"
        example_validate_coinbase_tx = validate_coinbase_tx(
            example_new_coinbase_transaction_2, example_block_index)
        self.assertEqual(False, example_validate_coinbase_tx)

        # Test invalid tx_ins count
        example_new_coinbase_transaction_2 = copy.deepcopy(
            example_new_coinbase_transaction)
        example_new_coinbase_transaction_2['tx_ins'].append(
            example_new_coinbase_transaction_2['tx_ins'][0])
        example_new_coinbase_transaction_2['id'] = get_transaction_id(
            example_new_coinbase_transaction_2)
        example_validate_coinbase_tx = validate_coinbase_tx(
            example_new_coinbase_transaction_2, example_block_index)
        self.assertEqual(False, example_validate_coinbase_tx)

        # Test invalid tx_in address
        example_new_coinbase_transaction_2 = copy.deepcopy(
            example_new_coinbase_transaction)
        example_new_coinbase_transaction_2['tx_ins'][0]['tx_out_index'] = 2
        example_new_coinbase_transaction_2['id'] = get_transaction_id(
            example_new_coinbase_transaction_2)
        example_validate_coinbase_tx = validate_coinbase_tx(
            example_new_coinbase_transaction_2, example_block_index)
        self.assertEqual(False, example_validate_coinbase_tx)

        # Test invalid number of txOuts
        example_new_coinbase_transaction_2 = copy.deepcopy(
            example_new_coinbase_transaction)
        example_new_coinbase_transaction_2['tx_outs'].append(
            example_new_coinbase_transaction_2['tx_outs'][0])
        example_new_coinbase_transaction_2['id'] = get_transaction_id(
            example_new_coinbase_transaction_2)
        example_validate_coinbase_tx = validate_coinbase_tx(
            example_new_coinbase_transaction_2, example_block_index)
        self.assertEqual(False, example_validate_coinbase_tx)

        # Test invalid coinbase amount in coinbase transaction
        example_new_coinbase_transaction_2 = copy.deepcopy(
            example_new_coinbase_transaction)
        example_new_coinbase_transaction_2['tx_outs'][0]['amount'] = COINBASE_AMOUNT - 1
        example_new_coinbase_transaction_2['id'] = get_transaction_id(
            example_new_coinbase_transaction_2)
        example_validate_coinbase_tx = validate_coinbase_tx(
            example_new_coinbase_transaction_2, example_block_index)
        self.assertEqual(False, example_validate_coinbase_tx)

        # Test whether the first tx in block is coinbase tx or not
        example_validate_coinbase_tx = validate_coinbase_tx(
            None, example_block_index)
        self.assertEqual(False, example_validate_coinbase_tx)

    def test_validate_block_transactions(self):
        # Creating valid block transactions
        valid_tx_kit_1 = self.create_valid_transaction_kit()
        example_tx_1 = valid_tx_kit_1[0]
        example_unspent_tx_outs_1 = valid_tx_kit_1[1]
        valid_tx_kit_2 = self.create_valid_transaction_kit()
        example_tx_2 = valid_tx_kit_2[0]
        example_unspent_tx_outs_2 = valid_tx_kit_2[1]

        # Creating a valid coinbase_tx
        example_address = "A61B5BE06CD7FE6D95064DAC98C97C9C8D128BEFACF7EA655D4EDF5B09B7DFAB6D059DD0A64B8C3CE9A11FEDC38143819BDF9CD4BC23EDCECFBAEB7DECACC81FE84CA7DE4AD33C89C9E848A5A8E8BDFD3BEA7BB3C4F81B4D"
        example_block_index = 1
        example_new_coinbase_transaction = new_coinbase_transaction(
            example_address, example_block_index)

        a_transactions = [example_new_coinbase_transaction, example_tx_1, example_tx_2]
        a_unspent_tx_outs = [example_unspent_tx_outs_1, example_unspent_tx_outs_2]

        # Testing valid block transactions
        example_validate_block_transactions = validate_block_transactions(a_transactions, a_unspent_tx_outs, example_block_index)
        self.assertEqual(True, example_validate_block_transactions)



if __name__ == '__main__':
    unittest.main()
