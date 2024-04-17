from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `create_time` SET DEFAULT '2024-04-12 21:39:10.328087';
        ALTER TABLE `user` MODIFY COLUMN `create_time` DATE NOT NULL  COMMENT '创建时间' DEFAULT '2024-04-12 21:39:10.328087';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `create_time` VARCHAR(64) NOT NULL  COMMENT '创建时间';
        ALTER TABLE `user` ALTER COLUMN `create_time` DROP DEFAULT;"""
