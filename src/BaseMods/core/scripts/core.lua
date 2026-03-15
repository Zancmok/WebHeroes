---@param prototypes table
---@return void
function _G.data:extend(prototypes)
    for _, v in ipairs(prototypes) do
        if type(v) ~= "table" then goto continue end
        if v.type == nil then goto continue end
        if type(v.type) ~= "string" then goto continue end
        if self.raw[v.type] == nil then goto continue end
        if v.name == nil then goto continue end
        if type(v.name) ~= "string" then goto continue end

        self.raw[v.type][v.name] = v

        ::continue::
    end
end

---@param prototype_type string
---@param prototype_name string
---@return table
function _G.data:get_prototype(prototype_type, prototype_name)
    if type(prototype_name) ~= "string" then return nil end
    if type(prototype_type) ~= "string" then return nil end
    if self.raw[prototype_type] == nil then return nil end

    return self.raw[prototype_type][prototype_name]
end

---@param prototype table
---@return string
function _G.data:id(prototype)
    if type(prototype) ~= "table" then return nil end

    return prototype.name
end

---@param prototype_type string
---@param prototype_name string
---@return string
function _G.data:id_of(prototype_type, prototype_name)
    return self:id(self:get_prototype(prototype_type, prototype_name))
end

_G.data.name_of = _G.data.id_of
