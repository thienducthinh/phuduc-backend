DROP DATABASE IF EXISTS OcoMainDB;

CREATE DATABASE OcoMainDB DEFAULT CHARACTER SET = 'utf8mb4';

USE OcoMainDB;

-- -- Drop existing tables to avoid conflicts
DROP TABLE IF EXISTS PriceBook;
DROP TABLE IF EXISTS Inventory;

DROP TABLE IF EXISTS InventoryTransaction;
DROP TABLE IF EXISTS Warehouse;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Supplier;


CREATE TABLE item_brand (
    brand_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL,
    brand_description TEXT
);

CREATE TABLE item_category (
    category_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    category_description TEXT
);

-- -- Create the Item table
CREATE TABLE item (
    item_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    brand_id INT(6) ZEROFILL,
    category_id INT(6) ZEROFILL,
    item_name VARCHAR(255) NOT NULL,
    item_description TEXT,
    FOREIGN KEY (brand_id) REFERENCES ItemBrand(brand_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES ItemCategory(category_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- -- Create the Supplier table
CREATE TABLE supplier (
    supplier_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(255),
    supplier_address VARCHAR(255) ,
    supplier_phone VARCHAR(15),
    supplier_email VARCHAR(100)
);

-- -- Create the Warehouse table
CREATE TABLE warehouse (
    warehouse_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    warehouse_name VARCHAR(255)
);

-- -- Create the Inventory table
CREATE TABLE inventory (
    inventory_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    item_id INT(6) ZEROFILL,
    warehouse_id INT(6) ZEROFILL,
    quantity INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- -- Create the InventoryTransaction table
CREATE TABLE inventory_transaction (
    transaction_id INT(9) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    warehouse_id INT(6) ZEROFILL,
    transaction_type ENUM('Purchase Order', 'Sales Order') NOT NULL,
    total_amount DECIMAL(10, 2),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE inventory_transaction_line (
    line_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT(6) ZEROFILL,
    item_id INT(6) ZEROFILL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2),
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (transaction_id) REFERENCES InventoryTransaction(transaction_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE price_book (
    price_book_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    business_id INT(6) ZEROFILL,
    description VARCHAR(255),
    price_type ENUM('Supplier', 'Customer 1', 'Customer 2', 'Customer 3') NOT NULL,
);

CREATE TABLE price_book_line (
    line_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    price_book_id INT(6) ZEROFILL,
    item_id INT(6) ZEROFILL,
    price DECIMAL(10, 2),
    FOREIGN KEY (price_book_id) REFERENCES PriceBook(price_book_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE purchase_order (
    purchase_order_id INT(9) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT(6) ZEROFILL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (purchase_order_id) REFERENCES InventoryTransaction(transaction_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE customer (
    customer_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    customer_address VARCHAR(255),
    customer_phone VARCHAR(15),
    customer_email VARCHAR(100),
    price_type ENUM('Customer 1', 'Customer 2', 'Customer 3') NOT NULL
);

CREATE TABLE sales_order (
    sales_order_id INT(9) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
    customer_id INT(6) ZEROFILL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sales_order_id) REFERENCES InventoryTransaction(transaction_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE    
);

CREATE TABLE inventory_adjustment (
    adjustment_id INT(9) ZEROFILL AUTO_INCREMENT PRIMARY KEY,    
    adjustment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (adjustment_id) REFERENCES InventoryTransaction(transaction_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

