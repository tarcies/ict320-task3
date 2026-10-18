IF NOT EXISTS (SELECT 1
               FROM   dbo.Users
               WHERE  Username = 'bob')
    INSERT  INTO dbo.Users (
        Username,
        PasswordHash,
        Role
    )
    VALUES                 ('bob', 'scrypt:32768:8:1$yRRRIwHtjiJZJpLX$2ed30c86e8d3d552fec1647ccce4beca265bc25b98671d64bcc06183bdbfdae3d4b498c83fbda78e5011b351ab32a8405b31ffbdb04a3ad6f532e5cc2fce59ed', 'field');

IF NOT EXISTS (SELECT 1
               FROM   dbo.Users
               WHERE  Username = 'admin')
    INSERT  INTO dbo.Users (
        Username,
        PasswordHash,
        Role
    )
    VALUES                 ('admin', 'scrypt:32768:8:1$RGOAtYi1uUShB4J8$59877ac7a344c7a3e2560f003997dff1886104da6c8f6dae03e8aaa12c86086c62995e58dc6101b4a07961b63a6eabc6adb276ae7b5c84fcfd2994255276e6ac', 'admin');