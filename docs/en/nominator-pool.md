# Nominator Pool

## Running the Validator in Nominator Pool Mode

1. Set up the hardware for the validator - you will need 8 vCPUs, 64GB memory, 1TB SSD, a fixed IP address, and 1Gb/s internet speed.

   For maintaining network stability, it's recommended to distribute validator nodes in different geographical locations worldwide rather than concentrating them in a single data center. You can use [this site](https://status.toncenter.com/) to assess the load of various locations. The map indicates high data center utilization in Europe, especially in Finland, Germany, and Paris. Therefore, using providers such as Hetzner and OVH is not recommended.

   > Ensure your hardware matches or exceeds the specifications above. Running the validator on insufficient hardware negatively impacts the network and could result in penalties.

   > Note that as of May 2021, Hetzner has prohibited mining on its servers, and this ban includes both PoW and PoS algorithms. Even installing a regular node may be considered a violation of their terms of service.

   > **Recommended providers include:** [Amazon](https://aws.amazon.com/), [DigitalOcean](https://www.digitalocean.com/), [Linode](https://www.linode.com/), [Alibaba Cloud](https://alibabacloud.com/), [Latitude](https://www.latitude.sh/).

2. Install and synchronize **mytonctrl** as described in the guide [here](https://github.com/ton-blockchain/mytonctrl/blob/master/docs/en/manual-ubuntu.md) — follow **only** steps 1, 2, and 3.

   You can also refer to this [Video Instruction](https://ton.org/docs/#/nodes/run-node) for additional help.

3. Transfer 1 TON to the validator wallet address shown in the `wl` list.

4. Use the `aw` command to activate your validator wallet.

5. Create two pools (for even and odd validation rounds):
   
   ```bash
   new_pool p1 0 1 1000 300000
   new_pool p2 0 1 1001 300000
   ```

   where:
    * `p1` is the pool name;
    * `0` % is the validator's reward share (e.g., use 40 for 40%);
    * `1` is the maximum number of nominators in the pool (should be <= 40);
    * `1000` TON is the minimum validator stake (should be >= 1K TON);
    * `300000` TON is the minimum nominator stake (should be >= 10K TON);

   > (!) Pool configurations do not have to be identical, you can add 1 to the minimum stake of one pool to make them different.

   > (!) Use https://tonmon.xyz/ to determine the current minimum validator stake.

6. Type `pools_list` to display pool addresses:

   ```bash
   pools_list
   Name  Status  Balance  Address
   p1    empty   0        0f98YhXA9wnr0d5XRXT-I2yH54nyQzn0tuAYC4FunT780qIT
   p2    empty   0        0f9qtmnzs2-PumMisKDmv6KNjNfOMDQG70mQdp-BcAhnV5jL
   ```

7. Send 1 TON to each pool and activate the pools:

   ```bash
   mg validator_wallet_001 0f98YhXA9wnr0d5XRXT-I2yH54nyQzn0tuAYC4FunT780qIT 1
   mg validator_wallet_001 0f9qtmnzs2-PumMisKDmv6KNjNfOMDQG70mQdp-BcAhnV5jL 1
   activate_pool p1
   activate_pool p2
   ```

8. Type `pools_list` to display pools:

   ```bash
   pools_list
   Name  Status  Balance      Address
   p1    active  0.731199733  kf98YhXA9wnr0d5XRXT-I2yH54nyQzn0tuAYC4FunT780v_W
   p2    active  0.731199806  kf9qtmnzs2-PumMisKDmv6KNjNfOMDQG70mQdp-BcAhnV8UO
   ```

9. Open each pool via the link "https://tonscan.org/nominator/<address_of_pool>" and verify pool configurations.

10. Proceed with the validator deposit to each pool:

    ```bash
    deposit_to_pool validator_wallet_001 <address_of_pool_1> 1005
    deposit_to_pool validator_wallet_001 <address_of_pool_2> 1005
    ```

   In these commands, `1005` TON is the deposit amount. Be aware that 1 TON will be deducted by the pool for processing the deposit.

11. Proceed with the nominator deposit to each pool:

    Visit the pool link (from **Step 9**) and click **ADD STAKE**. 
    You can also make a deposit using **mytonctrl**, using the following commands:

    ```bash
    mg nominator_wallet_001 <address_of_pool_1> 300001 -C d
    mg nominator_wallet_001 <address_of_pool_2> 300001 -C d
    ```

   > (!) The nominator wallet must be initialized in basechain (workchain 0).

   > (!) Keep in mind that the validator wallet and nominator wallet must be stored separately! The validator wallet should be stored on the server with the validator node to ensure processing of all system transactions. Meanwhile, the nominator wallet should be stored in your cold cryptocurrency wallet.

   > To withdraw a nominator deposit, send a transaction with the comment `w` to the pool address (attach 1 TON to process the transaction). You can also perform this action using **mytonctrl**.

12. Activate pool mode:

    ```bash
    set usePool true
    set stake null
    ```
    
13. Invite nominators to deposit into your pools. The participation in validation will commence automatically.

    > (!) Ensure that you have at least 200 TON/month in your validator wallet for operation fees.

## Pool Configuration

If you're intending to lend to yourself, use `new_pool p1 0 1 1000 300000` (maximum of 1 nominator, 0% validator share).

If you're creating a pool for numerous nominators, you might use something like this: `new_pool p1 40 40 10000 10000` (maximum of 40 nominators, 40% validator share, minimum participant stakes of 10K TON).

## Transitioning a Regular Validator to Nominator Pool Mode

1. Input `set stake 0` to discontinue election participation.

2. Await the return of both your stakes from the elector.

3. Proceed with the steps under "Running the Validator in Nominator Pool Mode" from the **4th step** onwards.

3. Proceed with the steps under "Running the Validator in Nominator Pool Mode" from the **4th step** onwards.