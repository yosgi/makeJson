
-- 链接标题临时表
CREATE TABLE `tmp_link_tags`  (
  `id`          INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `hash`        VARCHAR(255) NOT NULL, -- md5 link
  `link`        VARCHAR(255) NOT NULL DEFAULT '',
  `title`       VARCHAR(255) NOT NULL DEFAULT '',
  `description` VARCHAR(255) NOT NULL DEFAULT '',
  `keywords`    VARCHAR(255) NOT NULL DEFAULT '',
  `tags_hy`     TEXT,
  `tags_js`     TEXT,
  `created`     INT(10) UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_hash` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 用户标签临时表
CREATE TABLE `tmp_user_tags` (
  `uid`         INT(10) UNSIGNED NOT NULL,
  `eefocus_uid` INT(10) UNSIGNED NOT NULL,
  `email`       VARCHAR(255) NOT NULL,
  `tags_hy`     TEXT,
  `tags_js`     TEXT,
  `created`     INT(10) UNSIGNED NOT NULL DEFAULT '0',
  `updated`     INT(10) UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
