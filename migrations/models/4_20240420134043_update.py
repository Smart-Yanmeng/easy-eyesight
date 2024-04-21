from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `record` ADD `right_naked_eye` DOUBLE NOT NULL  COMMENT '右眼裸眼视力';
        ALTER TABLE `record` ADD `left_with_glasses` DOUBLE NOT NULL  COMMENT '左眼矫正视力';
        ALTER TABLE `record` ADD `right_with_glasses` DOUBLE NOT NULL  COMMENT '右眼矫正视力';
        ALTER TABLE `record` ADD `left_naked_eye` DOUBLE NOT NULL  COMMENT '左眼裸眼视力';
        ALTER TABLE `record` DROP COLUMN `naked_eye`;
        ALTER TABLE `record` DROP COLUMN `wear_glasses`;
        ALTER TABLE `record` ALTER COLUMN `create_time` SET DEFAULT '2024-04-20 05:40:43.391644';
        ALTER TABLE `user` ALTER COLUMN `create_time` SET DEFAULT '2024-04-20 05:40:43.389637';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `create_time` SET DEFAULT '2024-04-18 11:09:36.970297';
        ALTER TABLE `record` ADD `naked_eye` DOUBLE NOT NULL  COMMENT '裸眼视力';
        ALTER TABLE `record` ADD `wear_glasses` DOUBLE NOT NULL  COMMENT '戴眼镜视力';
        ALTER TABLE `record` DROP COLUMN `right_naked_eye`;
        ALTER TABLE `record` DROP COLUMN `left_with_glasses`;
        ALTER TABLE `record` DROP COLUMN `right_with_glasses`;
        ALTER TABLE `record` DROP COLUMN `left_naked_eye`;
        ALTER TABLE `record` ALTER COLUMN `create_time` SET DEFAULT '2024-04-18 11:09:36.972300';"""
