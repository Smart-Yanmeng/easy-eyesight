from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `record` (
    `record_id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    `wear_glasses` DOUBLE NOT NULL  COMMENT '戴眼镜视力',
    `naked_eye` DOUBLE NOT NULL  COMMENT '裸眼视力',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT '2024-04-18T11:09:32.226583',
    `user_id` BIGINT NOT NULL,
    CONSTRAINT `fk_record_user_562943cd` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        ALTER TABLE `user` ALTER COLUMN `create_time` SET DEFAULT '2024-04-18 11:09:32.224588';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `create_time` SET DEFAULT '2024-04-12 21:58:28.137559';
        DROP TABLE IF EXISTS `record`;"""
