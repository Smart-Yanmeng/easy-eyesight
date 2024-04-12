from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP FOREIGN KEY `fk_user_org_de743fce`;
        ALTER TABLE `org` RENAME COLUMN `orgId` TO `org_id`;
        ALTER TABLE `org` RENAME COLUMN `orgType` TO `org_type`;
        ALTER TABLE `org` RENAME COLUMN `orgName` TO `org_name`;
        ALTER TABLE `user` RENAME COLUMN `userId` TO `user_id`;
        ALTER TABLE `user` RENAME COLUMN `photoUrl` TO `photo_url`;
        ALTER TABLE `user` RENAME COLUMN `createTime` TO `create_time`;
        ALTER TABLE `user` RENAME COLUMN `orgId_id` TO `org_id`;
        ALTER TABLE `user` ADD CONSTRAINT `fk_user_org_07018d17` FOREIGN KEY (`org_id`) REFERENCES `org` (`org_id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP FOREIGN KEY `fk_user_org_07018d17`;
        ALTER TABLE `org` RENAME COLUMN `org_id` TO `orgId`;
        ALTER TABLE `org` RENAME COLUMN `org_name` TO `orgName`;
        ALTER TABLE `org` RENAME COLUMN `org_type` TO `orgType`;
        ALTER TABLE `user` RENAME COLUMN `user_id` TO `userId`;
        ALTER TABLE `user` RENAME COLUMN `create_time` TO `createTime`;
        ALTER TABLE `user` RENAME COLUMN `photo_url` TO `photoUrl`;
        ALTER TABLE `user` RENAME COLUMN `org_id` TO `orgId_id`;
        ALTER TABLE `user` ADD CONSTRAINT `fk_user_org_de743fce` FOREIGN KEY (`orgId_id`) REFERENCES `org` (`orgId`) ON DELETE CASCADE;"""
