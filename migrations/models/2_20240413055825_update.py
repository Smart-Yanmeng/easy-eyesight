from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `create_time` SET DEFAULT '2024-04-12 21:58:25.925685';
        ALTER TABLE `user` MODIFY COLUMN `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT '2024-04-12 21:58:25.925685';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `create_time` DATE NOT NULL  COMMENT '创建时间' DEFAULT '2024-04-12 21:39:28.109828';
        ALTER TABLE `user` ALTER COLUMN `create_time` SET DEFAULT '2024-04-12 21:39:28.109828';"""
