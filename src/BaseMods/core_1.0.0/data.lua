function _G.data:extend(prototypes)
    for _, v in ipairs(prototypes) do
        if type(v) ~= "table" then goto continue end
        if v.type == nil then goto continue end
        if type(v.type) ~= "string" then goto continue end
        if self.raw[v.type] == nil then goto continue end

        table.insert(self.raw, v)

        ::continue::
    end
end
