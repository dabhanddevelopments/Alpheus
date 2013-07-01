
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `alpheus`
--

-- --------------------------------------------------------

--
-- Table structure for table `administrator`
--

CREATE TABLE IF NOT EXISTS "administrator" (
  "id" int(11) NOT NULL,
  "name" varchar(50) NOT NULL,
  "contact_name" varchar(50) NOT NULL,
  "contact_number" varchar(50) NOT NULL,
  "fee" decimal(15,5) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auditor`
--

CREATE TABLE IF NOT EXISTS "auditor" (
  "id" int(11) NOT NULL,
  "name" varchar(50) NOT NULL,
  "contact_name" varchar(50) NOT NULL,
  "contact_number" varchar(50) NOT NULL,
  "fee" decimal(15,5) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `benchmark`
--

CREATE TABLE IF NOT EXISTS "benchmark" (
  "id" int(11) NOT NULL,
  "name" varchar(50) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `benchmarkhistory`
--

CREATE TABLE IF NOT EXISTS "benchmarkhistory" (
  "id" int(11) NOT NULL,
  "benchmark_id" int(11) NOT NULL,
  "date_type" varchar(1) NOT NULL,
  "value_date" date NOT NULL,
  "mtd" decimal(15,5) NOT NULL,
  "net_drawdown" decimal(15,5) NOT NULL,
  "si" decimal(15,5) NOT NULL,
  "ann_return1" decimal(4,2) NOT NULL,
  "ann_return3" decimal(4,2) NOT NULL,
  "ann_return5" decimal(4,2) NOT NULL,
  "ann_volatility1" decimal(4,2) NOT NULL,
  "ann_volatility3" decimal(4,2) NOT NULL,
  "ann_volatility5" decimal(4,2) NOT NULL,
  "sharpe_ratio1" decimal(4,2) NOT NULL,
  "sharpe_ratio3" decimal(4,2) NOT NULL,
  "sharpe_ratio5" decimal(4,2) NOT NULL,
  "alpha1" decimal(4,2) NOT NULL,
  "alpha3" decimal(4,2) NOT NULL,
  "alpha5" decimal(4,2) NOT NULL,
  "beta1" decimal(4,2) NOT NULL,
  "beta3" decimal(4,2) NOT NULL,
  "beta5" decimal(4,2) NOT NULL,
  "correlation1" decimal(4,2) NOT NULL,
  "correlation3" decimal(4,2) NOT NULL,
  "correlation5" decimal(4,2) NOT NULL,
  PRIMARY KEY ("id"),
  KEY "benchmarkhistory_9a65e30c" ("benchmark_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE IF NOT EXISTS "category" (
  "id" int(11) NOT NULL,
  "name" varchar(50) NOT NULL,
  "group" varchar(3) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE IF NOT EXISTS "client" (
  "id" int(11) NOT NULL,
  "first_name" varchar(50) NOT NULL,
  "last_name" varchar(50) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `clienthistory`
--

CREATE TABLE IF NOT EXISTS "clienthistory" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) DEFAULT NULL,
  "holding_id" int(11) DEFAULT NULL,
  "client_id" int(11) NOT NULL,
  "date_type" varchar(1) NOT NULL,
  "mtd" decimal(4,2) NOT NULL,
  "net_drawdown" decimal(15,5) NOT NULL,
  "ytd" decimal(15,5) NOT NULL,
  "si" decimal(15,5) NOT NULL,
  "ann_return1" decimal(4,2) NOT NULL,
  "ann_return3" decimal(4,2) NOT NULL,
  "ann_return5" decimal(4,2) NOT NULL,
  "ann_volatility1" decimal(4,2) NOT NULL,
  "ann_volatility3" decimal(4,2) NOT NULL,
  "ann_volatility5" decimal(4,2) NOT NULL,
  "sharpe_ratio1" decimal(4,2) NOT NULL,
  "sharpe_ratio3" decimal(4,2) NOT NULL,
  "sharpe_ratio5" decimal(4,2) NOT NULL,
  "alpha1" decimal(4,2) NOT NULL,
  "alpha3" decimal(4,2) NOT NULL,
  "alpha5" decimal(4,2) NOT NULL,
  "beta1" decimal(4,2) NOT NULL,
  "beta3" decimal(4,2) NOT NULL,
  "beta5" decimal(4,2) NOT NULL,
  "correlation1" decimal(4,2) NOT NULL,
  "correlation3" decimal(4,2) NOT NULL,
  "correlation5" decimal(4,2) NOT NULL,
  "euro_nav" decimal(20,2) NOT NULL,
  "value_date" date NOT NULL,
  "previous_nav" decimal(20,2) NOT NULL,
  "performance_fees_added_back" decimal(20,2) NOT NULL,
  "subscription_amount" decimal(20,2) NOT NULL,
  "redemption_amount" decimal(20,2) NOT NULL,
  "net_movement" decimal(20,2) NOT NULL,
  "gross_assets_after_subs_red" decimal(20,2) NOT NULL,
  "pending_nav" decimal(20,2) NOT NULL,
  "nav" decimal(20,2) NOT NULL,
  "no_of_units" decimal(20,2) NOT NULL,
  PRIMARY KEY ("id"),
  KEY "clienthistory_10400ffb" ("fund_id"),
  KEY "clienthistory_460919ce" ("holding_id"),
  KEY "clienthistory_4a4e8ffb" ("client_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `client_benchmark`
--

CREATE TABLE IF NOT EXISTS "client_benchmark" (
  "id" int(11) NOT NULL,
  "client_id" int(11) NOT NULL,
  "benchmark_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "client_id" ("client_id","benchmark_id"),
  KEY "client_benchmark_4a4e8ffb" ("client_id"),
  KEY "client_benchmark_9a65e30c" ("benchmark_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `country`
--

CREATE TABLE IF NOT EXISTS "country" (
  "id" int(11) NOT NULL,
  "name" varchar(50) NOT NULL,
  "code" varchar(3) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `countrybreakdown`
--

CREATE TABLE IF NOT EXISTS "countrybreakdown" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  "country_id" int(11) NOT NULL,
  "category_id" int(11) NOT NULL,
  "mtd" decimal(15,5) NOT NULL,
  "ytd" decimal(15,5) NOT NULL,
  "si" decimal(15,5) NOT NULL,
  "value_date" date NOT NULL,
  PRIMARY KEY ("id"),
  KEY "countrybreakdown_10400ffb" ("fund_id"),
  KEY "countrybreakdown_534dd89" ("country_id"),
  KEY "countrybreakdown_42dc49bc" ("category_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `currency`
--

CREATE TABLE IF NOT EXISTS "currency" (
  "id" int(11) NOT NULL,
  "name" varchar(50) NOT NULL,
  "code" varchar(3) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `currencyposition`
--

CREATE TABLE IF NOT EXISTS "currencyposition" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  "currency_id" int(11) NOT NULL,
  "nav" decimal(20,5) NOT NULL,
  "value_date" date NOT NULL,
  PRIMARY KEY ("id"),
  KEY "currencyposition_10400ffb" ("fund_id"),
  KEY "currencyposition_41f657b3" ("currency_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `custodian`
--

CREATE TABLE IF NOT EXISTS "custodian" (
  "id" int(11) NOT NULL,
  "name" varchar(50) NOT NULL,
  "contact_name" varchar(50) NOT NULL,
  "contact_number" varchar(50) NOT NULL,
  "performance_fee" decimal(15,5) NOT NULL,
  "management_fee" decimal(15,5) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `fund`
--

CREATE TABLE IF NOT EXISTS "fund" (
  "id" int(11) NOT NULL,
  "name" varchar(200) DEFAULT NULL,
  "aum" smallint(6) NOT NULL,
  "mtd" smallint(6) NOT NULL,
  "ytd" smallint(6) NOT NULL,
  "one_day_var" smallint(6) NOT NULL,
  "total_cash" smallint(6) NOT NULL,
  "usd_hedge" smallint(6) NOT NULL,
  "checks" smallint(6) NOT NULL,
  "unsettled" smallint(6) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `fundhistory`
--

CREATE TABLE IF NOT EXISTS "fundhistory" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  "date_type" varchar(1) NOT NULL,
  "mtd" decimal(4,2) NOT NULL,
  "net_drawdown" decimal(15,5) NOT NULL,
  "ytd" decimal(15,5) NOT NULL,
  "si" decimal(15,5) NOT NULL,
  "ann_return1" decimal(4,2) NOT NULL,
  "ann_return3" decimal(4,2) NOT NULL,
  "ann_return5" decimal(4,2) NOT NULL,
  "ann_volatility1" decimal(4,2) NOT NULL,
  "ann_volatility3" decimal(4,2) NOT NULL,
  "ann_volatility5" decimal(4,2) NOT NULL,
  "sharpe_ratio1" decimal(4,2) NOT NULL,
  "sharpe_ratio3" decimal(4,2) NOT NULL,
  "sharpe_ratio5" decimal(4,2) NOT NULL,
  "alpha1" decimal(4,2) NOT NULL,
  "alpha3" decimal(4,2) NOT NULL,
  "alpha5" decimal(4,2) NOT NULL,
  "beta1" decimal(4,2) NOT NULL,
  "beta3" decimal(4,2) NOT NULL,
  "beta5" decimal(4,2) NOT NULL,
  "correlation1" decimal(4,2) NOT NULL,
  "correlation3" decimal(4,2) NOT NULL,
  "correlation5" decimal(4,2) NOT NULL,
  "no_of_units" decimal(20,5) NOT NULL,
  "euro_nav" decimal(20,5) NOT NULL,
  "no_of_units_fund" decimal(20,5) NOT NULL,
  "euro_nav_fund" decimal(20,5) NOT NULL,
  "value_date" date NOT NULL,
  "previous_nav" decimal(20,2) NOT NULL,
  "performance_fees_added_back" decimal(20,2) NOT NULL,
  "subscription_amount" decimal(20,2) NOT NULL,
  "redemption_amount" decimal(20,2) NOT NULL,
  "net_movement" decimal(20,2) NOT NULL,
  "gross_assets_after_subs_red" decimal(20,2) NOT NULL,
  "long_portfolio" decimal(20,2) NOT NULL,
  "dividends_receivable" decimal(20,2) NOT NULL,
  "assets_subtotal" decimal(20,2) NOT NULL,
  "cash" decimal(20,2) NOT NULL,
  "accrued_interest" decimal(20,2) NOT NULL,
  "interest_receivable_on_banks" decimal(20,2) NOT NULL,
  "recv_for_transactions" decimal(20,2) NOT NULL,
  "nav_securities" decimal(20,2) NOT NULL,
  "nav_securities_total" decimal(20,2) NOT NULL,
  "nav_cash" decimal(20,2) NOT NULL,
  "nav_other_assets" decimal(20,2) NOT NULL,
  "other_liabilities" decimal(20,2) NOT NULL,
  "transaction_fees_payable" decimal(20,2) NOT NULL,
  "management_fees_payable" decimal(20,2) NOT NULL,
  "serv_act_fees_payable" decimal(20,2) NOT NULL,
  "administrator_fees_payable" decimal(20,2) NOT NULL,
  "auditor_fees_payable" decimal(20,2) NOT NULL,
  "capital_fees_payable" decimal(20,2) NOT NULL,
  "corporate_secretarial_payable" decimal(20,2) NOT NULL,
  "custodian_fees_payable" decimal(20,2) NOT NULL,
  "financial_statement_prep_payable" decimal(20,2) NOT NULL,
  "sub_advisory_fees_payable" decimal(20,2) NOT NULL,
  "performance_fees_payable" decimal(20,2) NOT NULL,
  "liabilities_subtotal" decimal(20,2) NOT NULL,
  "transaction_payable" decimal(20,2) NOT NULL,
  "total_net_asset_value" decimal(20,2) NOT NULL,
  "fet_valuation" decimal(20,2) NOT NULL,
  "management_fees" decimal(20,2) NOT NULL,
  "other_fees" decimal(20,2) NOT NULL,
  "trustee_fees" decimal(20,2) NOT NULL,
  "custodian_fees" decimal(20,2) NOT NULL,
  "auditor_fees" decimal(20,2) NOT NULL,
  "administrator_fees" decimal(20,2) NOT NULL,
  "performance_fees" decimal(20,2) NOT NULL,
  PRIMARY KEY ("id"),
  KEY "fundhistory_10400ffb" ("fund_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `fund_benchmark`
--

CREATE TABLE IF NOT EXISTS "fund_benchmark" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  "benchmark_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "fund_id" ("fund_id","benchmark_id"),
  KEY "fund_benchmark_10400ffb" ("fund_id"),
  KEY "fund_benchmark_9a65e30c" ("benchmark_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `fxhedge`
--

CREATE TABLE IF NOT EXISTS "fxhedge" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  "trade_date" date NOT NULL,
  "settlement_date" date NOT NULL,
  "buy_sell" smallint(6) NOT NULL,
  "currency_id" int(11) NOT NULL,
  "amount" decimal(20,5) NOT NULL,
  PRIMARY KEY ("id"),
  KEY "fxhedge_10400ffb" ("fund_id"),
  KEY "fxhedge_41f657b3" ("currency_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `fxrate`
--

CREATE TABLE IF NOT EXISTS "fxrate" (
  "id" int(11) NOT NULL,
  "value_date" date NOT NULL,
  "currency_id" int(11) NOT NULL,
  "fx_rate" decimal(15,5) NOT NULL,
  PRIMARY KEY ("id"),
  KEY "fxrate_41f657b3" ("currency_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `holding`
--

CREATE TABLE IF NOT EXISTS "holding" (
  "id" int(11) NOT NULL,
  "currency_id" int(11) NOT NULL,
  "country_id" int(11) NOT NULL,
  "sector_id" int(11) NOT NULL,
  "sub_sector_id" int(11) NOT NULL,
  "location_id" int(11) NOT NULL,
  "asset_class_id" int(11) NOT NULL,
  "name" varchar(50) NOT NULL,
  "isin" varchar(12) NOT NULL,
  "rep_code" varchar(50) NOT NULL,
  "description" longtext NOT NULL,
  "valoren" int(11) NOT NULL,
  "nav" decimal(20,2) NOT NULL,
  "interest_rate" decimal(20,5) NOT NULL,
  "current_price" decimal(20,8) NOT NULL,
  "no_of_units" decimal(20,2) NOT NULL,
  "weight" decimal(20,5) NOT NULL,
  "value_date" date NOT NULL,
  PRIMARY KEY ("id"),
  KEY "holding_41f657b3" ("currency_id"),
  KEY "holding_534dd89" ("country_id"),
  KEY "holding_94c48b8" ("sector_id"),
  KEY "holding_d7cad665" ("sub_sector_id"),
  KEY "holding_319d859" ("location_id"),
  KEY "holding_fed04f2e" ("asset_class_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `holdingbreakdown`
--

CREATE TABLE IF NOT EXISTS "holdingbreakdown" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  "category_id" int(11) NOT NULL,
  "mtd" decimal(15,5) NOT NULL,
  "ytd" decimal(15,5) NOT NULL,
  "si" decimal(15,5) NOT NULL,
  "value_date" date NOT NULL,
  PRIMARY KEY ("id"),
  KEY "holdingbreakdown_10400ffb" ("fund_id"),
  KEY "holdingbreakdown_42dc49bc" ("category_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `holdinghistory`
--

CREATE TABLE IF NOT EXISTS "holdinghistory" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  "holding_id" int(11) NOT NULL,
  "date_type" varchar(1) NOT NULL,
  "si" decimal(4,2) NOT NULL,
  "ytd" decimal(4,2) NOT NULL,
  "mtd" decimal(4,2) NOT NULL,
  "nav" decimal(20,5) NOT NULL,
  "weight" decimal(20,5) NOT NULL,
  "value_date" date NOT NULL,
  PRIMARY KEY ("id"),
  KEY "holdinghistory_10400ffb" ("fund_id"),
  KEY "holdinghistory_460919ce" ("holding_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `holding_client`
--

CREATE TABLE IF NOT EXISTS "holding_client" (
  "id" int(11) NOT NULL,
  "holding_id" int(11) NOT NULL,
  "client_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "holding_id" ("holding_id","client_id"),
  KEY "holding_client_460919ce" ("holding_id"),
  KEY "holding_client_4a4e8ffb" ("client_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `holding_fund`
--

CREATE TABLE IF NOT EXISTS "holding_fund" (
  "id" int(11) NOT NULL,
  "holding_id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "holding_id" ("holding_id","fund_id"),
  KEY "holding_fund_460919ce" ("holding_id"),
  KEY "holding_fund_10400ffb" ("fund_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `peer`
--

CREATE TABLE IF NOT EXISTS "peer" (
  "id" int(11) NOT NULL,
  "name" varchar(50) NOT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `peer_holding`
--

CREATE TABLE IF NOT EXISTS "peer_holding" (
  "id" int(11) NOT NULL,
  "peer_id" int(11) NOT NULL,
  "holding_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "peer_id" ("peer_id","holding_id"),
  KEY "peer_holding_2a3f6e04" ("peer_id"),
  KEY "peer_holding_460919ce" ("holding_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `subscriptionredemption`
--

CREATE TABLE IF NOT EXISTS "subscriptionredemption" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  "client_id" int(11) NOT NULL,
  "trade_date" date NOT NULL,
  "input_date" date NOT NULL,
  "no_of_units" decimal(20,5) NOT NULL,
  "sub_red" smallint(6) NOT NULL,
  "nav" decimal(20,5) NOT NULL,
  "percent_released" smallint(6) NOT NULL,
  PRIMARY KEY ("id"),
  KEY "subscriptionredemption_10400ffb" ("fund_id"),
  KEY "subscriptionredemption_4a4e8ffb" ("client_id")
) AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `trade`
--

CREATE TABLE IF NOT EXISTS "trade" (
  "id" int(11) NOT NULL,
  "holding_id" int(11) NOT NULL,
  "fund_id" int(11) DEFAULT NULL,
  "client_id" int(11) DEFAULT NULL,
  "currency_id" int(11) NOT NULL,
  "no_of_units" decimal(20,2) NOT NULL,
  "purchase_price" decimal(20,5) NOT NULL,
  "purchase_price_base" decimal(20,5) NOT NULL,
  "nav_purchase" decimal(20,5) NOT NULL,
  "fx_euro" decimal(20,8) NOT NULL,
  "trade_date" date NOT NULL,
  "settlement_date" date NOT NULL,
  PRIMARY KEY ("id"),
  KEY "trade_460919ce" ("holding_id"),
  KEY "trade_10400ffb" ("fund_id"),
  KEY "trade_4a4e8ffb" ("client_id"),
  KEY "trade_41f657b3" ("currency_id")
) AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `benchmarkhistory`
--
ALTER TABLE `benchmarkhistory`
  ADD CONSTRAINT "benchmark_id_refs_id_d0697a00" FOREIGN KEY ("benchmark_id") REFERENCES "benchmark" ("id");

--
-- Constraints for table `clienthistory`
--
ALTER TABLE `clienthistory`
  ADD CONSTRAINT "fund_id_refs_id_445f99f6" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id"),
  ADD CONSTRAINT "client_id_refs_id_87b6364" FOREIGN KEY ("client_id") REFERENCES "client" ("id"),
  ADD CONSTRAINT "holding_id_refs_id_89a7df7f" FOREIGN KEY ("holding_id") REFERENCES "holding" ("id");

--
-- Constraints for table `client_benchmark`
--
ALTER TABLE `client_benchmark`
  ADD CONSTRAINT "benchmark_id_refs_id_5e992786" FOREIGN KEY ("benchmark_id") REFERENCES "benchmark" ("id"),
  ADD CONSTRAINT "client_id_refs_id_89459b2f" FOREIGN KEY ("client_id") REFERENCES "client" ("id");

--
-- Constraints for table `countrybreakdown`
--
ALTER TABLE `countrybreakdown`
  ADD CONSTRAINT "fund_id_refs_id_feea09ef" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id"),
  ADD CONSTRAINT "category_id_refs_id_24b395ae" FOREIGN KEY ("category_id") REFERENCES "category" ("id"),
  ADD CONSTRAINT "country_id_refs_id_b9fd4ab3" FOREIGN KEY ("country_id") REFERENCES "country" ("id");

--
-- Constraints for table `currencyposition`
--
ALTER TABLE `currencyposition`
  ADD CONSTRAINT "fund_id_refs_id_dcc934a6" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id"),
  ADD CONSTRAINT "currency_id_refs_id_ffff3f6e" FOREIGN KEY ("currency_id") REFERENCES "currency" ("id");

--
-- Constraints for table `fundhistory`
--
ALTER TABLE `fundhistory`
  ADD CONSTRAINT "fund_id_refs_id_f3e41efc" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id");

--
-- Constraints for table `fund_benchmark`
--
ALTER TABLE `fund_benchmark`
  ADD CONSTRAINT "benchmark_id_refs_id_1b8a2138" FOREIGN KEY ("benchmark_id") REFERENCES "benchmark" ("id"),
  ADD CONSTRAINT "fund_id_refs_id_d9e0c957" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id");

--
-- Constraints for table `fxhedge`
--
ALTER TABLE `fxhedge`
  ADD CONSTRAINT "fund_id_refs_id_616ad6" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id"),
  ADD CONSTRAINT "currency_id_refs_id_9da98a62" FOREIGN KEY ("currency_id") REFERENCES "currency" ("id");

--
-- Constraints for table `fxrate`
--
ALTER TABLE `fxrate`
  ADD CONSTRAINT "currency_id_refs_id_96a97308" FOREIGN KEY ("currency_id") REFERENCES "currency" ("id");

--
-- Constraints for table `holding`
--
ALTER TABLE `holding`
  ADD CONSTRAINT "country_id_refs_id_98a4d9b4" FOREIGN KEY ("country_id") REFERENCES "country" ("id"),
  ADD CONSTRAINT "asset_class_id_refs_id_3721293b" FOREIGN KEY ("asset_class_id") REFERENCES "category" ("id"),
  ADD CONSTRAINT "currency_id_refs_id_b110b2a" FOREIGN KEY ("currency_id") REFERENCES "currency" ("id"),
  ADD CONSTRAINT "location_id_refs_id_3721293b" FOREIGN KEY ("location_id") REFERENCES "category" ("id"),
  ADD CONSTRAINT "sector_id_refs_id_3721293b" FOREIGN KEY ("sector_id") REFERENCES "category" ("id"),
  ADD CONSTRAINT "sub_sector_id_refs_id_3721293b" FOREIGN KEY ("sub_sector_id") REFERENCES "category" ("id");

--
-- Constraints for table `holdingbreakdown`
--
ALTER TABLE `holdingbreakdown`
  ADD CONSTRAINT "fund_id_refs_id_121b9310" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id"),
  ADD CONSTRAINT "category_id_refs_id_c2fd5c8d" FOREIGN KEY ("category_id") REFERENCES "category" ("id");

--
-- Constraints for table `holdinghistory`
--
ALTER TABLE `holdinghistory`
  ADD CONSTRAINT "fund_id_refs_id_895521cb" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id"),
  ADD CONSTRAINT "holding_id_refs_id_b372210" FOREIGN KEY ("holding_id") REFERENCES "holding" ("id");

--
-- Constraints for table `holding_client`
--
ALTER TABLE `holding_client`
  ADD CONSTRAINT "holding_id_refs_id_e87976f2" FOREIGN KEY ("holding_id") REFERENCES "holding" ("id"),
  ADD CONSTRAINT "client_id_refs_id_212b53a3" FOREIGN KEY ("client_id") REFERENCES "client" ("id");

--
-- Constraints for table `holding_fund`
--
ALTER TABLE `holding_fund`
  ADD CONSTRAINT "holding_id_refs_id_2ba66f4c" FOREIGN KEY ("holding_id") REFERENCES "holding" ("id"),
  ADD CONSTRAINT "fund_id_refs_id_e8e1a391" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id");

--
-- Constraints for table `peer_holding`
--
ALTER TABLE `peer_holding`
  ADD CONSTRAINT "holding_id_refs_id_f409f1d3" FOREIGN KEY ("holding_id") REFERENCES "holding" ("id"),
  ADD CONSTRAINT "peer_id_refs_id_210a2d3d" FOREIGN KEY ("peer_id") REFERENCES "peer" ("id");

--
-- Constraints for table `subscriptionredemption`
--
ALTER TABLE `subscriptionredemption`
  ADD CONSTRAINT "fund_id_refs_id_fd387d8" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id"),
  ADD CONSTRAINT "client_id_refs_id_2cadf5ce" FOREIGN KEY ("client_id") REFERENCES "client" ("id");

--
-- Constraints for table `trade`
--
ALTER TABLE `trade`
  ADD CONSTRAINT "holding_id_refs_id_6348cf8c" FOREIGN KEY ("holding_id") REFERENCES "holding" ("id"),
  ADD CONSTRAINT "client_id_refs_id_c83d06f7" FOREIGN KEY ("client_id") REFERENCES "client" ("id"),
  ADD CONSTRAINT "currency_id_refs_id_b514b389" FOREIGN KEY ("currency_id") REFERENCES "currency" ("id"),
  ADD CONSTRAINT "fund_id_refs_id_7cd4a4af" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id");

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
