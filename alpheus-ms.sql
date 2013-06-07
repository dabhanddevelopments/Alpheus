
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `alpheus`
--

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
-- Table structure for table `history`
--

CREATE TABLE IF NOT EXISTS "history" (
  "id" int(11) NOT NULL,
  "fund_id" int(11) NOT NULL,
  "category_id" int(11) NOT NULL,
  "benchmark_id" int(11) NOT NULL,
  "holding_id" int(11) NOT NULL,
  "peer_id" int(11) NOT NULL,
  "client_id" int(11) NOT NULL,
  "mtd" decimal(4,2) NOT NULL,
  "ytd" decimal(15,5) NOT NULL,
  "si" decimal(15,5) NOT NULL,
  "net_drawdown" decimal(15,5) DEFAULT NULL,
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
  "current_price" decimal(20,8) NOT NULL,
  "no_of_units" decimal(20,2) NOT NULL,
  "weight" decimal(20,5) NOT NULL,
  "euro_nav" decimal(20,2) NOT NULL,
  "value_date" date NOT NULL,
  PRIMARY KEY ("id"),
  KEY "history_10400ffb" ("fund_id"),
  KEY "history_42dc49bc" ("category_id"),
  KEY "history_9a65e30c" ("benchmark_id"),
  KEY "history_460919ce" ("holding_id"),
  KEY "history_2a3f6e04" ("peer_id"),
  KEY "history_4a4e8ffb" ("client_id")
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
  KEY "holding_94c48b8" ("sector_id"),
  KEY "holding_d7cad665" ("sub_sector_id"),
  KEY "holding_319d859" ("location_id"),
  KEY "holding_fed04f2e" ("asset_class_id")
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
-- Table structure for table `trade`
--

CREATE TABLE IF NOT EXISTS "trade" (
  "id" int(11) NOT NULL,
  "holding_id" int(11) NOT NULL,
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
) AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `history`
--
ALTER TABLE `history`
  ADD CONSTRAINT "benchmark_id_refs_id_f6a10df6" FOREIGN KEY ("benchmark_id") REFERENCES "benchmark" ("id"),
  ADD CONSTRAINT "category_id_refs_id_6a75b458" FOREIGN KEY ("category_id") REFERENCES "category" ("id"),
  ADD CONSTRAINT "client_id_refs_id_7a73c065" FOREIGN KEY ("client_id") REFERENCES "client" ("id"),
  ADD CONSTRAINT "fund_id_refs_id_2913ec0b" FOREIGN KEY ("fund_id") REFERENCES "fund" ("id"),
  ADD CONSTRAINT "holding_id_refs_id_8e92d7d0" FOREIGN KEY ("holding_id") REFERENCES "holding" ("id"),
  ADD CONSTRAINT "peer_id_refs_id_2913ec0b" FOREIGN KEY ("peer_id") REFERENCES "fund" ("id");

--
-- Constraints for table `holding`
--
ALTER TABLE `holding`
  ADD CONSTRAINT "asset_class_id_refs_id_3721293b" FOREIGN KEY ("asset_class_id") REFERENCES "category" ("id"),
  ADD CONSTRAINT "location_id_refs_id_3721293b" FOREIGN KEY ("location_id") REFERENCES "category" ("id"),
  ADD CONSTRAINT "sector_id_refs_id_3721293b" FOREIGN KEY ("sector_id") REFERENCES "category" ("id"),
  ADD CONSTRAINT "sub_sector_id_refs_id_3721293b" FOREIGN KEY ("sub_sector_id") REFERENCES "category" ("id");

--
-- Constraints for table `trade`
-- 
ALTER TABLE `trade`
  ADD CONSTRAINT "holding_id_refs_id_6348cf8c" FOREIGN KEY ("holding_id") REFERENCES "holding" ("id");

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
